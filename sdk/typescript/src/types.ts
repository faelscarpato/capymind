/**
 * Types for CapyMind SDK
 * Matches the AI contracts in ai/contracts/
 */

export interface SearchResult {
  query: string;
  total: number;
  limit?: number;
  offset?: number;
  results: SearchResultItem[];
}

export interface SearchResultItem {
  path: string;
  score: number;
  title?: string;
  snippet?: string;
  section?: string;
  doc_type?: string;
  status?: string;
  sensitivity?: string;
  canonical?: boolean;
  tags?: string[];
}

export interface ContextPack {
  query: string;
  pack_version: string;
  generated_at: string;
  summary?: string;
  sources: ContextSource[];
  notes?: string;
}

export interface ContextSource {
  path: string;
  chunk_index: number;
  score?: number;
  text?: string;
  metadata?: Record<string, any>;
}

export interface Project {
  id: string;
  name: string;
  slug: string;
  description: string;
  status: 'active' | 'experimental' | 'deprecated' | 'archived';
  domain?: string;
  repository?: string;
  tags?: string[];
  sensitivity?: string;
  canonical?: boolean;
  documentation?: string;
}

export interface Document {
  id: string;
  path: string;
  title: string;
  doc_type: string;
  domain?: string;
  status: string;
  tags?: string[];
  sensitivity?: string;
  canonical?: boolean;
  content?: string;
}
