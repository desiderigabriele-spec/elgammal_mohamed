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
  // Lingue: per ora solo italiano. Per aggiungere fr, de, ar basta inserirle qui
  // e creare le pagine in src/pages/<lingua>/. L'arabo usa dir="rtl" (vedi src/i18n/lingue.ts).
  i18n: {
    defaultLocale: 'it',
    locales: ['it'],
    routing: { prefixDefaultLocale: false },
  },
  integrations: [
    sitemap({
      filter: (page) => !page.includes('/404') && !page.includes('/anteprima'),
      i18n: { defaultLocale: 'it', locales: { it: 'it-IT' } },
    }),
  ],
  image: { responsiveStyles: false },
  prefetch: { prefetchAll: true, defaultStrategy: 'viewport' },
});
