import contextConfig from './config/contextSections.json';
import { MultiEngineContext } from './contextManager';

interface ContextSection {
    id: string;
    title: string | null;
    content?: string;
    enabled: boolean;
    priority: number;
    dynamic?: boolean;
    source?: string;
    conditional?: {
        source: string;
        path: string;
        required: boolean;
    };
    items?: Array<{
        label?: string;
        value?: string;
        path?: string;
        description?: string;
        type?: string;
        fallback?: any;
        critical?: boolean;
    }>;
    rules?: Array<{
        rule: string;
        details: string;
        critical: boolean;
    }>;
}

interface ContextConfig {
    version: string;
    contextSections: ContextSection[];
    formatting: {
        markdown: boolean;
        bullet_char: string;
        indent: string;
        section_spacing: string;
        label_value_separator: string;
    };
}

/**
 * Data-Driven Context Generator
 * Generates AI context messages from JSON configuration
 * AINLP Pattern: Configuration-driven, not hard-coded
 */
export class ContextGenerator {
    private config: ContextConfig;

    constructor() {
        this.config = contextConfig as ContextConfig;
    }

    /**
     * Generate context message from configuration and dynamic data
     */
    public generateContextMessage(multiEngineContext: MultiEngineContext): string {
        const sections: string[] = [];

        // Sort sections by priority
        const sortedSections = [...this.config.contextSections]
            .filter(section => section.enabled)
            .sort((a, b) => a.priority - b.priority);

        for (const section of sortedSections) {
            // Check conditional rendering
            if (section.conditional && !this.checkCondition(section.conditional, multiEngineContext)) {
                continue;
            }

            const sectionContent = this.renderSection(section, multiEngineContext);
            if (sectionContent) {
                sections.push(sectionContent);
            }
        }

        return sections.join(this.config.formatting.section_spacing);
    }

    /**
     * Render individual section based on type
     */
    private renderSection(section: ContextSection, context: MultiEngineContext): string {
        const parts: string[] = [];

        // Add title if present
        if (section.title) {
            parts.push(`## ${section.title}`);
        }

        // Add static content if present
        if (section.content) {
            parts.push(section.content);
        }

        // Render items (key-value pairs)
        if (section.items) {
            for (const item of section.items) {
                const rendered = this.renderItem(item, section, context);
                if (rendered) {
                    parts.push(rendered);
                }
            }
        }

        // Render rules (special formatting)
        if (section.rules) {
            for (const rule of section.rules) {
                const critical = rule.critical ? ' (CRITICAL)' : '';
                parts.push(`${this.config.formatting.bullet_char} **${rule.rule}**${critical} - ${rule.details}`);
            }
        }

        return parts.length > 0 ? parts.join('\n') + '\n' : '';
    }

    /**
     * Render individual item with dynamic data resolution
     */
    private renderItem(
        item: any,
        section: ContextSection,
        context: MultiEngineContext
    ): string | null {
        // Static item (path + description for architecture)
        if (item.path && item.description) {
            return `${this.config.formatting.bullet_char} **${item.path}**: ${item.description}`;
        }

        // Dynamic item (resolve from context)
        if (item.path && section.dynamic && section.source) {
            const value = this.resolveValue(item.path, context, section.source, item.fallback);
            if (value !== null) {
                const formattedValue = item.type === 'array' 
                    ? (Array.isArray(value) ? value.join(', ') : value)
                    : value;
                return `${this.config.formatting.bullet_char} **${item.label}**${this.config.formatting.label_value_separator}${formattedValue}`;
            }
        }

        // Static item (label + value)
        if (item.label && item.value) {
            const critical = item.critical ? ' (CRITICAL)' : '';
            return `${this.config.formatting.bullet_char} **${item.label}**${critical}${this.config.formatting.label_value_separator}${item.value}`;
        }

        return null;
    }

    /**
     * Resolve dynamic value from context using dot notation path
     */
    private resolveValue(
        path: string,
        context: MultiEngineContext,
        source: string,
        fallback: any
    ): any {
        try {
            // Get source object from context
            const sourceObj = this.getSourceObject(source, context);
            if (!sourceObj) {
                return fallback;
            }

            // Navigate path using dot notation
            const parts = path.split('.');
            let current: any = sourceObj;

            for (const part of parts) {
                if (current && typeof current === 'object' && part in current) {
                    current = current[part];
                } else {
                    return fallback;
                }
            }

            return current ?? fallback;

        } catch (error) {
            return fallback;
        }
    }

    /**
     * Get source object from multi-engine context
     */
    private getSourceObject(source: string, context: MultiEngineContext): any {
        switch (source) {
            case 'aiosContext':
                return context.aiosContext;
            case 'aiContextAutoLoad':
                return context.aiContextAutoLoad;
            case 'chatmodeRules':
                return context.chatmodeRules;
            case 'spatialMetadata':
                return context.spatialMetadata;
            default:
                return null;
        }
    }

    /**
     * Check if conditional section should be rendered
     */
    private checkCondition(
        condition: { source: string; path: string; required: boolean },
        context: MultiEngineContext
    ): boolean {
        const value = this.resolveValue(condition.path, context, condition.source, null);
        return condition.required ? value !== null : true;
    }

    /**
     * Get configuration version
     */
    public getConfigVersion(): string {
        return this.config.version;
    }

    /**
     * Reload configuration (for hot-reloading in dev mode)
     */
    public reloadConfig(): void {
        // In production, this would re-read the JSON file
        // For now, it's a no-op since config is bundled
        this.config = contextConfig as ContextConfig;
    }
}
