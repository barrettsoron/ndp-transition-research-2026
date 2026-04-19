/**
 * Derive section slugs and labels from the content collection at build time.
 * No hardcoded section lists — new date folders are picked up automatically.
 */

/** Labels for non-date sections. Date sections derive labels from their slug. */
const FIXED_LABELS: Record<string, string> = {
  'speeches': 'Avi Lewis — Speeches & Statements',
  'stephen-lewis': 'Stephen Lewis',
};

/** Descriptions for non-date sections. Date sections get a generic description. */
const FIXED_DESCRIPTIONS: Record<string, string> = {
  'speeches': 'Victory speech (EN/FR), leadership showcase, victory email to members',
  'stephen-lewis': 'Historical speeches and legacy context',
};

/** Special label overrides for specific date sections. */
const DATE_LABEL_OVERRIDES: Record<string, string> = {
  'march-29': 'March 29 — Convention Day',
};

const FIXED_SECTIONS = ['speeches', 'stephen-lewis'];
const CONVENTION_SECTIONS = ['march-26', 'march-27', 'march-28', 'march-27-28', 'march-29'];

/** Returns true if the slug is a dated section (e.g., "march-29", "april-13"). */
export function isDateSection(slug: string): boolean {
  return !FIXED_SECTIONS.includes(slug);
}

/** Returns true if the slug belongs to the convention period (March 27–29). */
export function isConventionSection(slug: string): boolean {
  return CONVENTION_SECTIONS.includes(slug);
}

/**
 * Extract unique section slugs from a content collection.
 * Sections are the first path segment of each article's id (e.g., "march-29" from "march-29/cbc-analysis").
 * Returns date sections sorted chronologically first, then fixed sections in a stable order.
 */
export function getSections(articles: { id: string }[]): string[] {
  const slugs = new Set<string>();
  for (const a of articles) {
    const section = a.id.split('/')[0];
    if (section) slugs.add(section);
  }

  const fixedOrder = ['speeches', 'stephen-lewis', 'transcript-archive'];
  const dateSections = [...slugs]
    .filter(s => !fixedOrder.includes(s))
    .sort(); // alphabetical sort puts dates in order (april-01 < april-02 < march-29 etc.)
  const fixed = fixedOrder.filter(s => slugs.has(s));

  // Sort date sections by parsing month and day for correct chronological order
  dateSections.sort((a, b) => {
    const toSortKey = (slug: string) => {
      const months: Record<string, number> = {
        january: 1, february: 2, march: 3, april: 4, may: 5, june: 6,
        july: 7, august: 8, september: 9, october: 10, november: 11, december: 12,
      };
      const parts = slug.split('-');
      const month = months[parts[0]] ?? 0;
      const day = parseInt(parts[1] ?? '0', 10);
      return month * 100 + day;
    };
    return toSortKey(a) - toSortKey(b);
  });

  return [...dateSections, ...fixed];
}

/**
 * Generate a human-readable label for a section slug.
 * Date sections (e.g., "april-02") become "April 2".
 * Fixed sections use their predefined labels.
 */
export function getSectionLabel(slug: string): string {
  if (DATE_LABEL_OVERRIDES[slug]) return DATE_LABEL_OVERRIDES[slug];
  if (FIXED_LABELS[slug]) return FIXED_LABELS[slug];

  // Parse date sections: "march-29" → "March 29", "april-02" → "April 2"
  const parts = slug.split('-');
  if (parts.length === 2) {
    const month = parts[0].charAt(0).toUpperCase() + parts[0].slice(1);
    const day = parseInt(parts[1], 10);
    if (!isNaN(day)) return `${month} ${day}`;
  }

  // Fallback: title-case the slug
  return slug.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

/**
 * Generate a short nav label for the header.
 * Date sections get abbreviated: "march-29" → "Mar 29".
 * Fixed sections get short names.
 */
export function getSectionNavLabel(slug: string): string {
  const shortFixed: Record<string, string> = {
    'speeches': 'Avi Lewis',
    'stephen-lewis': 'Stephen Lewis',
  };
  if (shortFixed[slug]) return shortFixed[slug];

  const parts = slug.split('-');
  if (parts.length === 2) {
    const month = parts[0].slice(0, 3).charAt(0).toUpperCase() + parts[0].slice(1, 3);
    const day = parseInt(parts[1], 10);
    if (!isNaN(day)) return `${month} ${day}`;
  }

  return slug;
}

const DATE_DESCRIPTIONS: Record<string, string> = {
  'march-26': 'Pre-convention; NDP Youth events',
  'march-27': 'Convention opens in Winnipeg',
  'march-28': 'Leadership showcase speeches',
  'march-29': 'Lewis wins on first ballot; election night coverage',
  'march-30': 'First wave of post-election reaction and commentary',
  'march-31': 'Death of Stephen Lewis; ballot result breakdown',
  'april-01': 'Archival Avi–Stephen interview resurfaces',
  'april-13': "Lewis's Parliament Hill debut; by-election coverage",
  'april-14': "Lewis's Parliament debut; Carney majority implications",
  'april-15': 'Parliamentary funding restored; NDP challenges Carney majority',
  'april-16': 'Sask NDP energy dispute; Alberta and western coverage',
  'april-17': 'Carney majority context; Lewis family profile',
  'april-18': "Lewis makes the case for democratic socialism; Parliament coverage",
};

/**
 * Get a description for a section. Used on the home page.
 */
export function getSectionDescription(slug: string): string {
  if (FIXED_DESCRIPTIONS[slug]) return FIXED_DESCRIPTIONS[slug];
  if (DATE_DESCRIPTIONS[slug]) return DATE_DESCRIPTIONS[slug];
  return 'Coverage and analysis';
}
