import it, { type Testi } from './it';
import en from './en';
import fr from './fr';
import de from './de';
import ar from './ar';
import type { Lingua } from '../lingue';

export const testi: Record<Lingua, Testi> = { it, en, fr, de, ar };
export const t = (l: Lingua): Testi => testi[l];
/** Sostituisce {chiave} con i valori dati: f('Fase {n}', { n: 3 }) -> 'Fase 3'. */
export const f = (s: string, v: Record<string, string | number>) => s.replace(/\{(\w+)\}/g, (_, k) => String(v[k] ?? `{${k}}`));
export type { Testi };
