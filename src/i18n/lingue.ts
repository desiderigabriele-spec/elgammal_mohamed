// Lingue del sito. L'italiano è la lingua principale (indirizzi senza prefisso);
// le altre hanno il prefisso: /en, /fr, /de, /ar.
// "dir" serve per l'arabo, che si legge da destra a sinistra: il CSS usa
// proprietà logiche (margin-inline, padding-inline...) così il layout si gira da solo.
export const lingue = {
  it: { nome: 'Italiano', breve: 'IT', locale: 'it-IT', og: 'it_IT', dir: 'ltr' },
  en: { nome: 'English', breve: 'EN', locale: 'en-GB', og: 'en_GB', dir: 'ltr' },
  fr: { nome: 'Français', breve: 'FR', locale: 'fr-FR', og: 'fr_FR', dir: 'ltr' },
  de: { nome: 'Deutsch', breve: 'DE', locale: 'de-DE', og: 'de_DE', dir: 'ltr' },
  ar: { nome: 'العربية', breve: 'AR', locale: 'ar', og: 'ar_AR', dir: 'rtl' },
} as const;

export type Lingua = keyof typeof lingue;
export const linguaPredefinita: Lingua = 'it';
export const codici = Object.keys(lingue) as Lingua[];
export const altreLingue = codici.filter((l) => l !== linguaPredefinita);

/** Lingua della pagina in corso (da usare in pagine e componenti: linguaDi(Astro)). */
export function linguaDi(A: { currentLocale?: string; params?: Record<string, string | undefined> }): Lingua {
  const l = (A.params?.lang ?? A.currentLocale ?? linguaPredefinita) as Lingua;
  return l in lingue ? l : linguaPredefinita;
}

/** Indirizzo di una pagina nella lingua data. percorso('/contatti', 'en') -> '/en/contatti'; '/' -> '/en'; '/#servizi' -> '/en#servizi'. */
export function percorso(p: string, l: Lingua): string {
  if (l === linguaPredefinita) return p;
  if (p === '/') return `/${l}`;
  if (p.startsWith('/#')) return `/${l}${p.slice(1)}`;
  return `/${l}${p}`;
}

/** Percorso "neutro" (senza lingua) della pagina in corso: '/en/muratura' -> '/muratura'. */
export function percorsoNeutro(pathname: string): string {
  const p = pathname.replace(/\.html$/, '').replace(/\/index$/, '/') || '/';
  const m = p.match(/^\/(en|fr|de|ar)(\/.*)?$/);
  if (!m) return p;
  return m[2] || '/';
}
