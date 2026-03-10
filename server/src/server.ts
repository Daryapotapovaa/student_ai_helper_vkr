import {
    createConnection,
    TextDocuments,
    ProposedFeatures,
    InitializeParams,
    TextDocumentSyncKind,
    InitializeResult
} from 'vscode-languageserver/node';
import { TextDocument } from 'vscode-languageserver-textdocument';
import { CompletionItem, CompletionItemKind } from 'vscode-languageserver/node';

const connection = createConnection(ProposedFeatures.all);
const documents: TextDocuments<TextDocument> = new TextDocuments(TextDocument);

connection.onInitialize((params: InitializeParams) => {
    connection.console.log('[LSP Server] Инициализация прошла успешно!');
    
    const result: InitializeResult = {
        capabilities: {
            textDocumentSync: TextDocumentSyncKind.Incremental,
            completionProvider: { resolveProvider: true }
        }
    };
    return result;
});

// Слушаем запрос от клиента
connection.onRequest('custom/getStudentHelp', async (params: any) => {
    connection.console.log('[LSP Server] Запрос получен. Генерирую ответ...');
    return '# HELLO WORLD (from LSP Server)';
});

// Обработчик автодополнения (срабатывает, когда печатаешь)

connection.onCompletion(
    (_textDocumentPosition: any): CompletionItem[] => {
        // Мы возвращаем массив наших предложений
        return [
            {
                label: 'StudentAI_Help', // То, что увидит пользователь в списке
                kind: CompletionItemKind.Text, // Иконка (текст, функция и т.д.)
                detail: 'Попросить помощи у ИИ', // Доп. описание
                documentation: 'Это вставит умную подсказку' // Документация (справа)
            }
        ];
    }
);


// Обработчик деталей автодополнения (нужен, раз мы включили resolveProvider)
connection.onCompletionResolve(
    (item: any): any => {
        return item;
    }
);

documents.listen(connection);
connection.listen();