export type PublishStatus = 'dry_run' | 'published' | 'failed';

export interface Article {
  id: string;
  title: string;
  slug: string;
  body: string;
  excerpt?: string;
  cover_image?: string;
  tags: string[];
  categories: string[];
}

export interface Publication {
  id: string;
  channel: string;
  article_id: string;
  status: PublishStatus;
  url?: string;
  external_id?: string;
  created_at: string;
}

export interface ConnectorCapabilities {
  publish: boolean;
  update: boolean;
  delete: boolean;
  verify: boolean;
  rollback: boolean;
  mediaUpload: boolean;
}

export interface Connector {
  name: string;
  authenticate(): Promise<void>;
  health(): Promise<{ status: string; detail?: string }>;
  capabilities(): ConnectorCapabilities;
  publish(article: Article, options?: Record<string, unknown>): Promise<Publication>;
  update?(publicationId: string, article: Article): Promise<Publication>;
  delete?(publicationId: string): Promise<void>;
  verify?(publicationId: string): Promise<boolean>;
  rollback?(publicationId: string): Promise<void>;
}
