import * as path from 'path';
import { workspace, ExtensionContext, commands, window, Position, Selection } from 'vscode';
import {
    LanguageClient,
    LanguageClientOptions,
    ServerOptions,
    TransportKind
} from 'vscode-languageclient/node';

let client: LanguageClient;

export function activate(context: ExtensionContext) {
    const serverModule = context.asAbsolutePath(
        path.join('server', 'out', 'server.js')
    );

    const debugOptions = { execArgv:['--nolazy', '--inspect=6009'] };

    const serverOptions: ServerOptions = {
        run: { module: serverModule, transport: TransportKind.ipc },
        debug: {
            module: serverModule,
            transport: TransportKind.ipc,
            options: debugOptions
        }
    };

    const clientOptions: LanguageClientOptions = {
        documentSelector:[{ scheme: 'file', language: 'python' }], // Важно: python
        synchronize: {
            fileEvents: workspace.createFileSystemWatcher('**/.clientrc')
        }
    };

    client = new LanguageClient(
        'studentAiServer',
        'Student AI Server',
        serverOptions,
        clientOptions
    );

    client.start();

    // Регистрация команды
    const disposable = commands.registerCommand('student-ai.insertComment', async () => {
        const editor = window.activeTextEditor;
        if (!editor) {
            window.showErrorMessage('Откройте файл .py!');
            return;
        }

        try {
            // Получаем ссылку на текущий документ
            const docUri = editor.document.uri.toString();

            // Отправляем запрос на сервер
            const aiResponse = await client.sendRequest<string>('custom/getStudentHelp', {
                uri: docUri 
            });

            if (!aiResponse) return;
            
            // Получаем текущую позицию курсора и текущую строку
            const position = editor.selection.active;
            const currentLine = editor.document.lineAt(position.line);
            
            // Вычисляем отступ
            const indent = currentLine.text.substring(0, currentLine.firstNonWhitespaceCharacterIndex);
            
            // Формируем текст для вставки
            const textToInsert = `\n${indent}${aiResponse}`;

            // Вставляем текст
            await editor.edit(editBuilder => {
                editBuilder.insert(currentLine.range.end, textToInsert);
            });

            // Вычисляем новую позицию курсора
            const linesAdded = textToInsert.split('\n');
            const lastLineLength = linesAdded[linesAdded.length - 1].length;
            
            const newPosition = new Position(
                position.line + linesAdded.length - 1, 
                lastLineLength
            );
            
            // Снимаем выделение и ставим курсор на новую позицию
            editor.selection = new Selection(newPosition, newPosition);

        } catch (error) {
            window.showErrorMessage(`Ошибка общения с LSP: ${error}`);
        }
    });

    context.subscriptions.push(disposable);
}

export function deactivate(): Thenable<void> | undefined {
    if (!client) {
        return undefined;
    }
    return client.stop();
}