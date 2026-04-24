/**
 * Example: Build a context pack for grounding an answer
 */

import { CapyMind } from '../src/index.js';

const client = new CapyMind({
  baseUrl: 'http://localhost:54321/functions/v1/capymind-api',
  apiKey: process.env.CAPYMIND_API_KEY || 'your-api-key'
});

async function main() {
  const query = 'What is the anti-prompt-injection policy?';
  const pack = await client.contextPack(query, 5);
  console.log('Context pack generated:');
  console.log('Query:', pack.query);
  console.log('Sources:');
  for (const src of pack.sources) {
    console.log(`- ${src.path} [chunk ${src.chunk_index}]: ${src.text?.substring(0, 60)}...`);
  }
}

main();
