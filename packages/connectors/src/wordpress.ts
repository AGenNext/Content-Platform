import type { Article, Connector, ConnectorCapabilities, Publication } from './index';

export class WordPressConnector implements Connector {
  name = 'wordpress';

  async authenticate(): Promise<void> {
    if (!process.env.WORDPRESS_URL) throw new Error('WORDPRESS_URL is required');
  }

  async health() {
    return { status: process.env.WORDPRESS_URL ? 'configured' : 'missing_credentials' };
  }

  capabilities(): ConnectorCapabilities {
    return { publish: true, update: true, delete: false, verify: true, rollback: false, mediaUpload: true };
  }

  async publish(article: Article, options: Record<string, unknown> = {}): Promise<Publication> {
    const dryRun = options.dry_run !== false;
    return {
      id: `wordpress_${article.id}`,
      channel: 'wordpress',
      article_id: article.id,
      status: dryRun ? 'dry_run' : 'published',
      url: `${process.env.WORDPRESS_URL || 'https://example.com'}/${article.slug}`,
      created_at: new Date().toISOString(),
    };
  }
}
