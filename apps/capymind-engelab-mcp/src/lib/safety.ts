export const SAFETY_NOTICE =
  'Material for study, reference, prompt engineering and technical organization only. It is not an executive project, technical report, legal validation, ART/RRT, approval document or substitute for a qualified professional review.';

export function withSafetyNotice<T extends Record<string, unknown>>(payload: T): T & { safety_notice: string } {
  return {
    ...payload,
    safety_notice: SAFETY_NOTICE,
  };
}

export function normalizeLimit(value: number | undefined, fallback = 5, max = 20): number {
  if (!Number.isFinite(value)) return fallback;
  const rounded = Math.floor(Number(value));
  return Math.min(Math.max(rounded, 1), max);
}

export function normalizeQuery(value: string): string {
  return value.trim().replace(/\s+/g, ' ');
}
