# El Gammal · Impresa edile — sito

Sito statico in [Astro](https://astro.build), pubblicabile su Vercel.

## Comandi
```bash
npm install
npm run dev        # sviluppo su http://localhost:4321
npm run build      # crea il sito in dist/
npx astro preview  # guarda la versione finale
npm test           # prove automatiche (con il preview acceso)
```

## Dove si cambiano le cose
- **Dati dell'impresa** (telefono, WhatsApp, email, P.IVA, scheda Google, comuni serviti): `src/data/impresa.ts`.
  Finché un dato è `null`, il sito mostra un segnaposto ben visibile.
- **Modulo contatti**: se `moduloEndpoint` è vuoto, il modulo apre WhatsApp con il messaggio già scritto e "(dal sito)".
  Per ricevere anche email, inserire l'indirizzo di un servizio come Formspree o Web3Forms.
- **Servizi** (testi, domande frequenti, foto): `src/data/servizi.ts`.
- **Foto**: `src/assets/foto/`. Quelle attuali sono provvisorie (CC0 da StockSnap, elenco in `crediti.json`)
  e vanno sostituite con le foto vere dei cantieri. La pagina `/lavori` resta fuori da Google (`noindex`)
  finché non ha foto vere.
- **Indirizzo del sito**: variabile `SITE_URL` (o `astro.config.mjs`), serve per sitemap e dati strutturati.
- **Lingue**: `src/i18n/lingue.ts`. Il CSS usa proprietà logiche, quindi l'arabo (`dir="rtl"`) si gira da solo.

## Materiale di progetto
`progetto/` contiene lo studio, il marchio, i concept, le schermate di verifica e i prompt per le immagini.
