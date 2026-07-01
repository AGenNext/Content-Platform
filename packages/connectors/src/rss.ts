import type { Article, Connector, ConnectorCapabilities, Publication } from './index';

export class RssConnector implements Connector {
  name = 'rss';
  async authenticate() {}
  async health() { return { status: 'ready' }; }
  capabilities(): ConnectorCapabilities {
    return { publish: true, update: true, delete: false, verify: true, rollback: false, mediaUpload: false };
  }
  async publish(article: Article): Promise<Publication> {
    return {
      id: `rss_${article.id}`,
      channel: 'rss',
      article_id: article.id,
      status: 'published',
      url: `/rss/${article.slug}.xml`,
      created_at: new Date().toISOString(),
    };
  }
}
