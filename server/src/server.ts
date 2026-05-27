import {
    createConnection,
    TextDocuments,
    ProposedFeatures,
    InitializeParams,
    TextDocumentSyncKind,
    Diagnostic,
    DiagnosticSeverity,
    CodeAction,
    CodeActionKind,
    CodeActionParams,
    TextEdit,
    WorkspaceEdit,
    Position
} from 'vscode-languageserver/node';
import { TextDocument } from 'vscode-languageserver-textdocument';
import OpenAI from 'openai';

const connection = createConnection(ProposedFeatures.all);
const documents: TextDocuments<TextDocument> = new TextDocuments(TextDocument);

// Считываем настройки из .env
const API_BASE_URL = process.env.API_BASE_URL || 'https://openrouter.ai/api/v1';
const API_KEY = process.env.API_KEY || 'local-key'; 
const MODELS_ENV_STRING = process.env.MODEL_NAME || 'openai/gpt-oss-20b:free';
const MODELS_LIST = MODELS_ENV_STRING.split(',').map(m => m.trim());

const openai = new OpenAI({
    baseURL: API_BASE_URL,
    apiKey: API_KEY,
    defaultHeaders: {
        "HTTP-Referer": "https://github.com/StudentAI",
        "X-Title": "Student AI Helper", 
    }
});

connection.onInitialize((params: InitializeParams) => {
    connection.console.log(`[LSP Server] Инициализация... URL: ${API_BASE_URL}`);
    return {
        capabilities: {
            textDocumentSync: TextDocumentSyncKind.Incremental,
            codeActionProvider: true
        }
    };
});

// Проверка кода при сохранении файла
documents.onDidSave(async (change) => {
    connection.console.log(`[LSP Server] Файл сохранен. Запуск ИИ-проверки...`);
    const document = change.document;
    const HELP_MODE = process.env.HELP_MODE || 'advice';

    // Нумеруем строки кода
    const lines = document.getText().split('\n');
    const numberedCode = lines.map((line, index) => `${index}: ${line}`).join('\n');

    // Системный промпт
    const systemPrompt = `
        Ты — опытный, терпеливый преподаватель Python и наставник для новичков.
        Твоя задача — найти главную ошибку или логическую недоработку в коде студента.
        Все объяснения пиши только на русском языке.
        Пользователь пришлет код с номерами строк.
        
        ПРАВИЛА ДЛЯ ФОРМИРОВАНИЯ ПОДСКАЗКИ (поле "message"):
        1. КАТЕГОРИЧЕСКИ ЗАПРЕЩАЕТСЯ дублировать стандартные ошибки интерпретатора Python (например, "SyntaxError", "NameError").
        2. Объясни суть проблемы простым, человеческим языком. Начни с того, ЧТО именно не так.
        3. Кратко объясни ПОЧЕМУ это важно. Напомни правило языка Python (например, "В Python все блоки внутри цикла должны быть выделены отступом").
        4. Дай наводящий совет, как это исправить, но НЕ пиши сам исправленный код внутри текста сообщения.
        5. Объем сообщения: 2-3 ясных предложения.
        
        Ты ДОЛЖЕН ответить СТРОГО в формате JSON без markdown разметки и лишнего текста:
        {
        "hasError": true или false,
        "line": <номер строки с ошибкой (число)>,
        "message": "<подробное педагогическое объяснение ошибки и совет>",
        "suggestedCode": "<исправленный фрагмент кода или null>"
        }
        Если ошибок нет, верни {"hasError": false}.
    `;

    let aiAnswerRaw = '';
    for (const currentModel of MODELS_LIST) {
        try {
            const completion = await openai.chat.completions.create({
                model: currentModel,
                messages:[
                    { role: "system", content: systemPrompt },
                    { role: "user", content: numberedCode }
                ]
            }, { timeout: 15000 });

            aiAnswerRaw = completion.choices[0]?.message?.content || '';
            break; // Выход из цикла при успешном ответе
        } catch (error: any) {
            connection.console.log(`[Warning] Ошибка модели ${currentModel}: ${error.message}`);
        }
    }

    if (!aiAnswerRaw) return;

    try {
        // Очищаем ответ от markdown
        const cleanJson = aiAnswerRaw.replace(/```json/g, '').replace(/```/g, '').trim();
        const aiResult = JSON.parse(cleanJson);
        connection.console.log(aiResult);
        // Очищаем подчеркивания при отсутсвии ошибок
        if (!aiResult.hasError) {
            connection.sendDiagnostics({ uri: document.uri, diagnostics:[] });
            return;
        }

        const errorLine = aiResult.line;
        
        // Создаем волнистое подчеркивание
        const diagnostic: Diagnostic = {
            severity: DiagnosticSeverity.Warning,
            range: {
                start: Position.create(errorLine, 0),
                end: Position.create(errorLine, lines[errorLine].length)
            },
            message: `🤖 ИИ: ${aiResult.message}`,
            source: 'StudentAI',
            data: { 
                mode: HELP_MODE, 
                message: aiResult.message, 
                code: aiResult.suggestedCode 
            }
        };

        // Отправляем диагностику в VS Code
        connection.sendDiagnostics({ uri: document.uri, diagnostics: [diagnostic] });

    } catch (e) {
        connection.console.log(`[Error] Не удалось распарсить JSON от ИИ: ${aiAnswerRaw}`);
    }
});

// Обработка нажатия на лампочку
connection.onCodeAction((params: CodeActionParams) => {
    const ourDiagnostics = params.context.diagnostics.filter(d => d.source === 'StudentAI');
    if (ourDiagnostics.length === 0) return[];

    const actions: CodeAction[] =[];
    const document = documents.get(params.textDocument.uri);
    if (!document) return[];

    for (const diagnostic of ourDiagnostics) {
        const data = diagnostic.data as any; // Извлекаем сохраненные данные от ИИ
        const errorLineNum = diagnostic.range.start.line;
        const currentLineText = document.getText({
            start: Position.create(errorLineNum, 0),
            end: Position.create(errorLineNum + 1, 0)
        });
        
        // Вычисляем отступ для вставки
        const indentMatch = currentLineText.match(/^\s*/);
        const indent = indentMatch ? indentMatch[0] : '';

        if (data.mode === 'code' && data.code) {
            const action = CodeAction.create(
                "🛠️ Применить исправление от ИИ",
                CodeActionKind.QuickFix
            );
            // Заменяем текущую строку с ошибкой на исправленный код от ИИ
            const edit = TextEdit.replace(diagnostic.range, `${indent}${data.code}`);
            action.edit = { changes: { [params.textDocument.uri]: [edit] } };
            action.diagnostics = [diagnostic];
            actions.push(action);
        }
    }

    return actions; 
});

// Очистка ошибок при изменении кода
documents.onDidChangeContent((change) => {
    connection.sendDiagnostics({ uri: change.document.uri, diagnostics:[]})})

// Запускаем слушателей
documents.listen(connection);
connection.listen();