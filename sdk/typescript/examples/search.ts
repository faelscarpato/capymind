/**
 * Example: Basic search using CapyMind SDK
 */

import { CapyMind } from '../src/index.js';

const client = new CapyMind({
  baseUrl: 'http://localhost:54321/functions/v1/capymind-api', // local dev
  apiKey: process.env.CAPYMIND_API_KEY || 'your-api-key'
});

async function main() {
  try {
    const result = await client.search('CapyMind retrieval safety', 5);
    console.log('Search results:');
    for (const r of result.results) {
      console.log(`- ${r.path} (score: ${r.score})`);
    }
  } catch (err: any) {
    console.error('Error:', err.message);
  }
}

main();
