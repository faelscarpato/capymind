/**
 * CapyMind TypeScript SDK
 *
 * Provides typed methods for interacting with CapyMind API and MCP tools.
 */

import { createClient } from '@supabase/supabase-js';
import { SearchResult, ContextPack, Project, Document } from './types';

export interface CapyMindConfig {
  baseUrl: string;
  apiKey: string;
}

export class CapyMind {
  private baseUrl: string;
  private apiKey: string;

  constructor(config: CapyMindConfig) {
    this.baseUrl = config.baseUrl.replace(/\/$/, ''); // strip trailing slash
    this.apiKey = config.apiKey;
  }

  /**
   * Perform a document search.
   * @param query Search query
   * @param limit Max results (default 10)
   */
  async search(query: string, limit = 10): Promise<SearchResult> {
    const url = `${this.baseUrl}/v1/search`;
    const resp = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`
      },
      body: JSON.stringify({ query, limit })
    });
    if (!resp.ok) {
      throw new Error(`Search failed: ${resp.status} ${resp.statusText}`);
    }
    return resp.json();
  }

  /**
   * Build a context pack for grounding.
   */
  async contextPack(query: string, limit = 5): Promise<ContextPack> {
    const url = `${this.baseUrl}/v1/context-pack`;
    const resp = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`
      },
      body: JSON.stringify({ query, limit })
    });
    if (!resp.ok) {
      throw new Error(`Context pack failed: ${resp.status} ${resp.statusText}`);
    }
    return resp.json();
  }

  async getProject(slug: string): Promise<Project> {
    const url = `${this.baseUrl}/v1/projects/${encodeURIComponent(slug)}`;
    const resp = await fetch(url, {
      headers: { 'Authorization': `Bearer ${this.apiKey}` }
    });
    if (!resp.ok) {
      throw new Error(`Get project failed: ${resp.status}`);
    }
    return resp.json();
  }

  async getDocument(id: string): Promise<Document> {
    const url = `${this.baseUrl}/v1/documents/${encodeURIComponent(id)}`;
    const resp = await fetch(url, {
      headers: { 'Authorization': `Bearer ${this.apiKey}` }
    });
    if (!resp.ok) {
      throw new Error(`Get document failed: ${resp.status}`);
    }
    return resp.json();
  }

  async health(): Promise<{status: string; timestamp: string}> {
    const url = `${this.baseUrl}/v1/health`;
    const resp = await fetch(url);
    return resp.json();
  }
}

export default CapyMind;
