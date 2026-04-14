import {
    createConnection,
    TextDocuments,
    ProposedFeatures,
    InitializeParams,
    TextDocumentSyncKind,
    InitializeResult
} from 'vscode-languageserver/node';
import { TextDocument } from 'vscode-languageserver-textdocument';
import OpenAI from 'openai';

const connection = createConnection(ProposedFeatures.all);
const documents: TextDocuments<TextDocument> = new TextDocuments(TextDocument);

// API ключ
const OPENROUTER_API_KEY = process.env.API_KEY;

const openai = new OpenAI({
    baseURL: 'https://openrouter.ai/api/v1',
    apiKey: OPENROUTER_API_KEY,
    defaultHeaders: {
        "HTTP-Referer": "https://github.com/StudentAI", // Требование OpenRouter (любая ссылка)
        "X-Title": "Student AI Helper", // Название твоего проекта
    }
});

connection.onInitialize((params: InitializeParams) => {
    connection.console.log('[LSP Server] Инициализация OpenRouter...');
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

    const systemPrompt = `
    Ты — преподаватель Python.
    Найди ошибку в коде или дай совет.
    Ответь одним предложением на русском языке.
    Начни ответ с символа #.
    `;

    try {
        const completion = await openai.chat.completions.create({
            model: "openai/gpt-oss-20b:free",
            messages: [
                { role: "system", content: systemPrompt },
                { role: "user", content: studentCode }
            ],
        });

        const aiAnswer = completion.choices[0].message.content;
        connection.console.log('[LSP Server] Ответ получен!');
        return aiAnswer;

    } catch (error) {
        connection.console.log(`[Error] API Error: ${error}`);
        return `# Ошибка сети: ${error}`;
    }
});

// Заглушки
connection.onCompletion(() => []);
connection.onCompletionResolve((item) => item);
documents.listen(connection);
connection.listen();