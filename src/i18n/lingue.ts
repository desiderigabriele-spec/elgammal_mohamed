// Lingue del sito. Oggi solo italiano; le altre sono pronte da attivare.
// "dir" serve per l'arabo, che si legge da destra a sinistra: il CSS usa
// proprietà logiche (margin-inline, padding-inline...) così il layout si gira da solo.
export const lingue = {
  it: { nome: 'Italiano', locale: 'it-IT', dir: 'ltr', attiva: true },
  fr: { nome: 'Français', locale: 'fr-FR', dir: 'ltr', attiva: false },
  de: { nome: 'Deutsch', locale: 'de-DE', dir: 'ltr', attiva: false },
  ar: { nome: 'العربية', locale: 'ar', dir: 'rtl', attiva: false },
} as const;

export type Lingua = keyof typeof lingue;
export const linguaPredefinita: Lingua = 'it';
