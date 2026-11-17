import type { Servizio } from '../servizi';
// Testi di un servizio in un'altra lingua: tutto tranne slug, numero, foto e note interne.
export type TestoServizio = Pick<Servizio, 'nome' | 'breve' | 'title' | 'description' | 'h1' | 'spessore' | 'fotoAlt' | 'intro' | 'problema' | 'soluzione' | 'passi' | 'prova' | 'faq'>;
export type TestiServizi = Record<string, TestoServizio>;
