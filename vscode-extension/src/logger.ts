import * as vscode from 'vscode';

export class AIOSLogger {
    private outputChannel: vscode.OutputChannel;
    private isDebugEnabled: boolean;

    constructor(context: vscode.ExtensionContext) {
        this.outputChannel = vscode.window.createOutputChannel('AIOS');
        this.isDebugEnabled = vscode.workspace.getConfiguration('aios').get('debug.enabled', false);
        
        context.subscriptions.push(this.outputChannel);
        
        // Listen for configuration changes
        vscode.workspace.onDidChangeConfiguration(e => {
            if (e.affectsConfiguration('aios.debug.enabled')) {
                this.isDebugEnabled = vscode.workspace.getConfiguration('aios').get('debug.enabled', false);
            }
        });
    }

    private formatMessage(level: string, message: string, ...args: any[]): string {
        const timestamp = new Date().toISOString();
        const formattedArgs = args.length > 0 ? ' ' + args.map(arg => 
            typeof arg === 'object' ? JSON.stringify(arg, null, 2) : String(arg)
        ).join(' ') : '';
        
        return `[${timestamp}] [${level}] ${message}${formattedArgs}`;
    }

    private log(level: string, message: string, ...args: any[]): void {
        const formattedMessage = this.formatMessage(level, message, ...args);
        this.outputChannel.appendLine(formattedMessage);
        
        // Also log to console in debug mode
        if (this.isDebugEnabled) {
            console.log(formattedMessage);
        }
    }

    info(message: string, ...args: any[]): void {
        this.log('INFO', message, ...args);
    }

    warn(message: string, ...args: any[]): void {
        this.log('WARN', message, ...args);
    }

    error(message: string, ...args: any[]): void {
        this.log('ERROR', message, ...args);
        
        // Show error in UI if debug is enabled
        if (this.isDebugEnabled) {
            vscode.window.showErrorMessage(`AIOS Error: ${message}`);
        }
    }

    debug(message: string, ...args: any[]): void {
        if (this.isDebugEnabled) {
            this.log('DEBUG', message, ...args);
        }
    }

    show(): void {
        this.outputChannel.show();
    }

    clear(): void {
        this.outputChannel.clear();
    }
}
