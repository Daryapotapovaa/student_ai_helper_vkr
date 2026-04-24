import {
    createConnection,
    TextDocuments,
    ProposedFeatures,
    InitializeParams,
    TextDocumentSyncKind
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
    connection.console.log(`[LSP Server] Загружен список моделей (Fallback): ${MODELS_LIST.join(' -> ')}`);
    
    return {
        capabilities: {
            textDocumentSync: TextDocumentSyncKind.Incremental,
            completionProvider: { resolveProvider: true }
        }
    };
});

connection.onRequest('custom/getStudentHelp', async (params: any) => {
    connection.console.log('[LSP Server] Запрос получен. Ожидание ответа...');

    const fileUri = params.uri;
    const document = documents.get(fileUri);

    if (!document) return '# Ошибка: файл не найден.';

    const studentCode = document.getText();

    // Считывааем режим работы из .env
    const HELP_MODE = process.env.HELP_MODE || 'advice';

    // Формируем промпты для разных режимов
    const systemPromptAdvice = `
    Ты — помощник преподавателя Python.
    Найди ошибку в коде или дай совет студенту, как продолжить.
    Ответь одним предложением на русском языке.
    Начни ответ с символа #. Никакого кода не пиши, только текстовую подсказку.
    `;

    const systemPromptCode = `
    Ты — помощник преподавателя Python.
    Найди ошибку в коде или логическое незавершение и предложи исправленный вариант.
    Формат ответа: сначала краткий комментарий с объяснением (начни строку с #), а на следующей строке напиши сам исправленный код только для того фрагмента, где была найдена ошибка.
    Не пиши приветствий и лишнего текста, выдай только комментарий и код.
    `;

    // Выбираем нужный промпт
    const systemPrompt = HELP_MODE === 'code' ? systemPromptCode : systemPromptAdvice;

    let lastError: any = null;

    // Обращение к моделям
    for (const currentModel of MODELS_LIST) {
        try {
            connection.console.log(`[LSP Server] Попытка генерации с моделью: ${currentModel} (Режим: ${HELP_MODE})`);
            
            const completion = await openai.chat.completions.create(
                {
                    model: currentModel,
                    messages:[
                        { role: "system", content: systemPrompt },
                        { role: "user", content: studentCode }
                    ]
                },
                { timeout: 10000 }
            );

            const aiAnswer = completion.choices[0]?.message?.content || '# Ошибка: пустой ответ от ИИ';
            connection.console.log(`[LSP Server] Успешный ответ получен!`);
            
            return aiAnswer;

        } catch (error: any) {
            connection.console.log(`[Warning] Модель ${currentModel} недоступна: ${error.message}.`);
            lastError = error;
        }
    }

    if (lastError && lastError.message.includes('ECONNREFUSED')) {
         return `# Ошибка: Локальный сервер ИИ не запущен (${API_BASE_URL}).`;
    }
    
    return `# Ошибка сети: Не удалось получить ответ. Последняя ошибка: ${lastError?.message || 'Неизвестная ошибка'}`;
});


// Заглушки
connection.onCompletion(() => []);
connection.onCompletionResolve((item) => item);
documents.listen(connection);
connection.listen();