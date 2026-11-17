// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Indirizzo pubblico del sito: cambiarlo quando c'è il dominio definitivo
// (oppure impostare SITE_URL su Vercel).
const SITE = process.env.SITE_URL || 'https://elgammalmohamed.vercel.app';

export default defineConfig({
  site: SITE,
  trailingSlash: 'never',
  build: { format: 'file' },
  // Lingue: italiano senza prefisso, le altre in /en, /fr, /de, /ar (pagine in src/pages/[lang]/).
  // L'arabo usa dir="rtl" (vedi src/i18n/lingue.ts).
  i18n: {
    defaultLocale: 'it',
    locales: ['it', 'en', 'fr', 'de', 'ar'],
    routing: { prefixDefaultLocale: false },
  },
  integrations: [
    sitemap({
      filter: (page) => !page.includes('/404'),
      i18n: { defaultLocale: 'it', locales: { it: 'it-IT', en: 'en-GB', fr: 'fr-FR', de: 'de-DE', ar: 'ar' } },
    }),
  ],
  image: { responsiveStyles: false },
  prefetch: { prefetchAll: true, defaultStrategy: 'viewport' },
});
