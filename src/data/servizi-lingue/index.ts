import { servizi, type Servizio } from '../servizi';
import type { Lingua } from '../../i18n/lingue';
import type { TestiServizi } from './tipo';
import en from './en';
import fr from './fr';
import de from './de';
import ar from './ar';

const traduzioni: Partial<Record<Lingua, TestiServizi>> = { en, fr, de, ar };

/** I servizi nella lingua data: stessi slug, numeri e foto; testi tradotti. Le note interne restano solo in italiano. */
export function serviziIn(l: Lingua): Servizio[] {
  const tr = traduzioni[l];
  if (!tr) return servizi;
  return servizi.map((s) => {
    const x = tr[s.slug];
    if (!x) throw new Error(`Traduzione mancante: ${l}/${s.slug}`);
    return { ...s, ...x, nota: undefined };
  });
}
