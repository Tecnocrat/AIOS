"""
AIOS Knowledge Ingestion - Microsoft Provider
=============================================

AINLP.dendritic[ai/ingestion/providers/microsoft]{msft,azure,windows,vscode}

Microsoft ecosystem knowledge provider.
Aggregates RSS feeds from Windows Dev, Azure AI, VS Code, GitHub blogs.
"""

from ..protocol import KnowledgeProvider, KnowledgeSource
from ..sources.base import SourceConfig
from ..sources.rss import RSSSourceAdapter


# Microsoft feed configurations
MICROSOFT_FEEDS = {
    "windows_dev": SourceConfig(
        name="Windows Developer Blog",
        url="https://blogs.windows.com/windowsdeveloper/feed/",
        category="agentic_windows",
        priority="high",
        tags=["windows", "copilot", "sdk", "winui"],
    ),
    "azure_ai": SourceConfig(
        name="Azure AI Blog",
        url="https://azure.microsoft.com/en-us/blog/feed/",
        category="azure_ai_foundry",
        priority="high",
        tags=["azure", "ai", "foundry", "models"],
        filter_keywords=[
            "AI", "Copilot", "GPT", "LLM", "Agent",
            "Foundry", "OpenAI", "Machine Learning"
        ],
    ),
    "dotnet": SourceConfig(
        name=".NET Blog",
        url="https://devblogs.microsoft.com/dotnet/feed/",
        category="dotnet_evolution",
        priority="medium",
        tags=["dotnet", "csharp", "aspnet", "maui"],
    ),
    "vscode": SourceConfig(
        name="VS Code Blog",
        url="https://code.visualstudio.com/feed.xml",
        category="developer_tools",
        priority="medium",
        tags=["vscode", "extensions", "copilot"],
    ),
    "github": SourceConfig(
        name="GitHub Blog",
        url="https://github.blog/feed/",
        category="developer_tools",
        priority="medium",
        tags=["github", "copilot", "actions", "codespaces"],
        filter_keywords=[
            "Copilot", "AI", "Agent", "Actions", "Codespaces"
        ],
    ),
}


class MicrosoftProvider(KnowledgeProvider):
    """
    Microsoft ecosystem knowledge provider.

    Sources:
    - Windows Developer Blog (agentic_windows)
    - Azure AI Blog (azure_ai_foundry)
    - .NET Blog (dotnet_evolution)
    - VS Code Blog (developer_tools)
    - GitHub Blog (developer_tools)
    """

    def __init__(self, feeds: dict[str, SourceConfig] | None = None):
        """
        Initialize Microsoft provider.

        Args:
            feeds: Optional custom feed configurations
        """
        self._feeds = feeds or MICROSOFT_FEEDS
        self._sources: list[KnowledgeSource] = []

        # Create RSS adapters for each feed
        for feed_id, config in self._feeds.items():
            if config.enabled:
                adapter = RSSSourceAdapter(
                    provider_name=self.name,
                    config=config,
                )
                self._sources.append(adapter)

    @property
    def name(self) -> str:
        return "microsoft"

    @property
    def description(self) -> str:
        return (
            "Microsoft ecosystem knowledge ingestion. "
            "Aggregates Windows Dev, Azure AI, .NET, VS Code, and GitHub blogs."
        )

    def get_sources(self) -> list[KnowledgeSource]:
        return self._sources

    def get_feed_config(self, feed_id: str) -> SourceConfig | None:
        """Get configuration for a specific feed."""
        return self._feeds.get(feed_id)


# Convenience function for standalone use
async def fetch_microsoft_feeds(
    max_items: int = 10,
    priority_filter: str | None = None,
) -> list:
    """
    Fetch from all Microsoft feeds.

    Args:
        max_items: Max items per feed
        priority_filter: Filter by priority ("high", "medium", "low")

    Returns:
        List of IngestionResult
    """
    provider = MicrosoftProvider()
    results = await provider.fetch_all(max_items=max_items)

    if priority_filter:
        for result in results:
            result.items = [
                item for item in result.items
                if item.priority.value == priority_filter
            ]

    return results


if __name__ == "__main__":
    import asyncio

    async def main():
        print("Testing Microsoft Provider...")
        results = await fetch_microsoft_feeds(max_items=5)

        for result in results:
            print(f"\n{result.source_name}:")
            print(f"  Items: {len(result.items)}")
            if result.errors:
                print(f"  Errors: {result.errors}")
            for item in result.items[:3]:
                print(f"  - {item.title[:60]}...")

    asyncio.run(main())
