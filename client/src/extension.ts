import * as path from 'path';
import { workspace, ExtensionContext, commands, window } from 'vscode';
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

    const debugOptions = { execArgv: ['--nolazy', '--inspect=6009'] };

    const serverOptions: ServerOptions = {
        run: { module: serverModule, transport: TransportKind.ipc },
        debug: {
            module: serverModule,
            transport: TransportKind.ipc,
            options: debugOptions
        }
    };

    const clientOptions: LanguageClientOptions = {
        documentSelector: [{ scheme: 'file', language: 'python' }], // Важно: python
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
            window.showErrorMessage('Открой файл .py!');
            return;
        }

        try {
            const aiResponse = await client.sendRequest<string>('custom/getStudentHelp', {});
            editor.edit(editBuilder => {
                editBuilder.insert(editor.selection.active, aiResponse);
            });
        } catch (error) {
            window.showErrorMessage(`Ошибка: ${error}`);
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