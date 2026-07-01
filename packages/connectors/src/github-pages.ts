import type { Article, Connector, ConnectorCapabilities, Publication } from './index';

export class GitHubPagesConnector implements Connector {
  name = 'github_pages';
  async authenticate(): Promise<void> {
    if (!process.env.GITHUB_REPO) throw new Error('GITHUB_REPO is required');
  }
  async health() { return { status: process.env.GITHUB_REPO ? 'configured' : 'missing_credentials' }; }
  capabilities(): ConnectorCapabilities {
    return { publish: true, update: true, delete: true, verify: true, rollback: false, mediaUpload: false };
  }
  async publish(article: Article, options: Record<string, unknown> = {}): Promise<Publication> {
    const dryRun = options.dry_run !== false;
    return {
      id: `github_pages_${article.id}`,
      channel: 'github_pages',
      article_id: article.id,
      status: dryRun ? 'dry_run' : 'published',
      url: `/${process.env.GITHUB_CONTENT_PATH || 'content/posts'}/${article.slug}.md`,
      created_at: new Date().toISOString(),
    };
  }
}
