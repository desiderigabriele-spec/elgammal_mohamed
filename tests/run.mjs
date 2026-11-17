// Prove automatiche del sito. Uso: avviare "npx astro preview" (porta 4321) e poi "npm test".
import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const axeSource = readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');

const BASE = process.env.BASE_URL || 'http://localhost:4321';
const PAGINE = ['/', '/muratura', '/intonaci-imbiancatura', '/rasatura-pareti', '/cartongesso', '/impianti', '/facciate', '/ristrutturazioni-chiavi-in-mano', '/lavori', '/chi-siamo', '/dove-lavoriamo', '/contatti', '/privacy', '/cookie',
  // un campione delle altre lingue (l'arabo si legge da destra a sinistra)
  '/en', '/fr/muratura', '/de/contatti', '/ar', '/ar/rasatura-pareti', '/en/chi-siamo'];
const MOBILE = { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true };
const DESKTOP = { viewport: { width: 1440, height: 900 } };
// script iniettati prima di ogni pagina (come testo: una funzione perderebbe le variabili esterne)
const CONSENSO = (v) => ({ content: `try { localStorage.setItem('elg-lingua', 'it'); localStorage.setItem('elg-consenso-v1', JSON.stringify({ esterni: ${v ? 'true' : 'false'}, data: 'test' })); } catch (e) {}` });
const SOLO_LINGUA = { content: `try { localStorage.setItem('elg-lingua', 'it'); } catch (e) {}` };

let ok = 0, ko = 0;
const check = (cond, nome, info = '') => { if (cond) { ok++; console.log('  ✓', nome); } else { ko++; console.log('  ✗', nome, info); } };

const b = await chromium.launch();

console.log('\n1 · Nessun errore in console, contrasto (axe), aree da toccare, righe lunghe');
for (const [nomeDev, opt] of [['telefono', MOBILE], ['computer', DESKTOP]]) {
  const ctx = await b.newContext(opt);
  await ctx.addInitScript(CONSENSO(false));
  for (const path of PAGINE) {
    const p = await ctx.newPage(); const errs = [];
    p.on('pageerror', (e) => errs.push(e.message));
    p.on('console', (m) => { if (m.type() === 'error') errs.push(m.text()); });
    await p.goto(BASE + path, { waitUntil: 'networkidle' });
    check(errs.length === 0, `${nomeDev} ${path}: console pulita`, errs.join(' | '));
    if (nomeDev === 'telefono') {
      await p.addScriptTag({ content: axeSource });
      const r = await p.evaluate(async () => (await window.axe.run(document, { runOnly: ['color-contrast', 'target-size', 'image-alt', 'label', 'link-name', 'button-name', 'html-has-lang', 'document-title', 'heading-order'] })).violations.map((v) => `${v.id}(${v.nodes.length}): ${v.nodes.slice(0, 2).map((n) => n.target.join(' ')).join(', ')}`));
      check(r.length === 0, `${path}: accessibilità e contrasto`, r.join(' || '));
      const piccoli = await p.evaluate(() => [...document.querySelectorAll('a.btn, button, .dock a, .chip, summary, input, select, textarea')]
        .filter((e) => e.offsetParent !== null && !e.closest('[hidden]')).map((e) => { const r = e.getBoundingClientRect(); return { t: (e.textContent || e.name || e.tagName).trim().slice(0, 30), w: Math.round(r.width), h: Math.round(r.height) }; })
        .filter((x) => x.h < 44 || x.w < 44));
      check(piccoli.length === 0, `${path}: aree da toccare ≥ 44 px`, JSON.stringify(piccoli.slice(0, 4)));
      const testoPiccolo = await p.evaluate(() => [...document.querySelectorAll('main p, main li, main a, main span, main dd, main dt, main label, footer p, footer a')]
        .filter((e) => e.offsetParent !== null && e.childElementCount === 0 && e.textContent.trim() && !e.closest('svg') && !e.closest('.vh'))
        .map((e) => ({ t: e.textContent.trim().slice(0, 30), s: parseFloat(getComputedStyle(e).fontSize) })).filter((x) => x.s < 16));
      check(testoPiccolo.length === 0, `${path}: testo ≥ 16 px`, JSON.stringify(testoPiccolo.slice(0, 4)));
    } else {
      const lunghe = await p.evaluate(() => [...document.querySelectorAll('main p')].filter((e) => e.offsetParent !== null && e.textContent.length > 120).map((e) => {
        const cs = getComputedStyle(e); const ch = parseFloat(cs.fontSize) * 0.5; return Math.round(e.getBoundingClientRect().width / ch);
      }).filter((n) => n > 75));
      check(lunghe.length === 0, `${path}: righe non troppo lunghe`, JSON.stringify(lunghe));
    }
    await p.close();
  }
  await ctx.close();
}

console.log('\n2 · Menu del telefono');
{
  const ctx = await b.newContext(MOBILE); await ctx.addInitScript(CONSENSO(false));
  const p = await ctx.newPage(); await p.goto(BASE + '/');
  const drawer = p.locator('#drawer');
  check(await drawer.isHidden(), 'menu chiuso all\'inizio');
  await p.click('#burger');
  check(await drawer.isVisible(), 'il bottone Menu apre il menu');
  check((await drawer.locator('a').count()) >= 11, 'il menu contiene servizi e pagine');
  await p.keyboard.press('Escape');
  check(await drawer.isHidden(), 'Esc chiude il menu');
  await p.click('#burger'); await drawer.locator('a[href="/facciate"]').click(); await p.waitForURL('**/facciate');
  check(p.url().endsWith('/facciate'), 'un link del menu porta alla pagina giusta');
  await ctx.close();
}

console.log('\n3 · Barra di contatto e WhatsApp');
{
  const ctx = await b.newContext(MOBILE); await ctx.addInitScript(CONSENSO(false));
  const p = await ctx.newPage(); await p.goto(BASE + '/');
  const dock = p.locator('.dock');
  await p.evaluate(() => scrollTo(0, innerHeight * 1.5)); await p.waitForTimeout(400);
  check(await dock.isVisible(), 'tasti tondi WhatsApp ed email visibili sul telefono (dopo l\'hero)');
  const hrefs = await dock.locator('a').evaluateAll((as) => as.map((a) => a.getAttribute('href')));
  check(hrefs.length === 2 && hrefs.every(Boolean), 'WhatsApp ed email a un tocco', JSON.stringify(hrefs));
  check(await p.locator('header .mob .btn-p').isVisible(), 'bottone "Sopralluogo" sempre in alto sul telefono');
  await p.evaluate(() => scrollTo(0, document.body.scrollHeight / 2));
  check(await dock.isVisible(), 'i tasti restano visibili mentre scorri');
  const d = await b.newContext(DESKTOP); const pd = await d.newPage(); await pd.goto(BASE + '/');
  await pd.evaluate(() => scrollTo(0, innerHeight * 1.5)); await pd.waitForTimeout(400);
  check(await pd.locator('.dock').isVisible(), 'sul computer ci sono i tasti WhatsApp ed email');
  check(await pd.locator('.menu .btn-p').isVisible(), 'bottone "Sopralluogo gratuito" sempre in alto sul computer');
  await d.close(); await ctx.close();
}

console.log('\n4 · Modulo');
{
  const ctx = await b.newContext(MOBILE); await ctx.addInitScript(CONSENSO(false));
  const p = await ctx.newPage(); await p.goto(BASE + '/contatti');
  const f = p.locator('#contatti-form');
  await f.locator('button[type=submit]').click();
  check(await f.locator('[data-err]').isVisible(), 'modulo vuoto: spiega cosa manca');
  check(await p.evaluate(() => document.activeElement?.getAttribute('name')) === 'nome', 'il cursore va sul campo mancante');
  await f.locator('[name=nome]').fill('Mario Prova');
  await f.locator('[name=contatto]').fill('333 0000000');
  await f.locator('[name=tipo]').selectOption('Facciate');
  await f.locator('[name=messaggio]').fill('Facciata di un condominio di 4 piani');
  // numero di prova: simula il sito con WhatsApp configurato
  await p.evaluate(() => { const el = document.querySelector('#contatti-form'); el.dataset.conf = JSON.stringify({ ...JSON.parse(el.dataset.conf), endpoint: null, wa: '390000000000' }); });
  let waUrl = '';
  await p.route('https://wa.me/**', (r) => { waUrl = r.request().url(); r.abort(); });
  await f.locator('button[type=submit]').click(); await p.waitForTimeout(500);
  const testo = decodeURIComponent(waUrl.split('text=')[1] || '');
  check(waUrl.startsWith('https://wa.me/390000000000'), 'invio: apre WhatsApp con il messaggio pronto', waUrl);
  check(testo.includes('(dal sito)') && testo.includes('Mario Prova') && testo.includes('Facciate'), 'il messaggio contiene "(dal sito)" e i dati', testo);
  // con un indirizzo di invio configurato
  const p2 = await ctx.newPage(); await p2.goto(BASE + '/contatti');
  let corpo = null;
  await p2.route('https://invio.example/**', async (r) => { corpo = JSON.parse(r.request().postData()); await r.fulfill({ status: 200, body: '{}', contentType: 'application/json' }); });
  await p2.evaluate(() => { const el = document.querySelector('#contatti-form'); el.dataset.conf = JSON.stringify({ ...JSON.parse(el.dataset.conf), endpoint: 'https://invio.example/f', wa: null }); });
  const f2 = p2.locator('#contatti-form');
  await f2.locator('[name=nome]').fill('Anna'); await f2.locator('[name=contatto]').fill('anna@example.com');
  await f2.locator('button[type=submit]').click(); await p2.waitForTimeout(500);
  check(corpo && corpo._subject.includes('(dal sito)'), 'invio via servizio email: oggetto con "(dal sito)"', JSON.stringify(corpo));
  check(await f2.locator('[data-ok]').isVisible(), 'conferma di invio mostrata');
  await ctx.close();
}

console.log('\n5 · Cookie');
{
  const ctx = await b.newContext(MOBILE); await ctx.addInitScript(SOLO_LINGUA);
  const p = await ctx.newPage(); const google = [];
  p.on('request', (r) => { if (/google\.com|gstatic|googleapis|facebook|analytics/.test(r.url())) google.push(r.url()); });
  await p.goto(BASE + '/contatti', { waitUntil: 'networkidle' });
  const ck = p.locator('#ck');
  check(await ck.isVisible(), 'al primo ingresso compare la scelta sui cookie');
  const [bn, bs] = [ck.locator('[data-ck=no]'), ck.locator('[data-ck=si]')];
  const [rn, rs] = [await bn.boundingBox(), await bs.boundingBox()];
  check(Math.abs(rn.width - rs.width) < 2 && Math.abs(rn.height - rs.height) < 2 && (await bn.getAttribute('class')) === (await bs.getAttribute('class')), '"Accetta" e "Rifiuta" uguali per forma e grandezza');
  check((await ck.locator('input[type=checkbox]:checked').count()) === 0, 'nessuna casella già spuntata');
  check(google.length === 0, 'prima della scelta nessuna chiamata a Google o a statistiche', google.join(','));
  await bn.click();
  check(await ck.isHidden(), '"Rifiuta" chiude il banner');
  await p.reload({ waitUntil: 'networkidle' });
  check(await ck.isHidden(), 'la scelta viene ricordata');
  check((await p.locator('[data-map] iframe').count()) === 0 && google.length === 0, 'dopo "Rifiuta" la mappa Google non si carica');
  await p.locator('footer [data-cookie-open]').click();
  check(await ck.isVisible(), '"Preferenze cookie" riapre la scelta');
  await p.route('https://www.google.com/**', (r) => r.fulfill({ status: 200, body: '<html></html>', contentType: 'text/html' }));
  await ck.locator('[data-ck=si]').click(); await p.waitForTimeout(300);
  check((await p.locator('[data-map] iframe').count()) === 1, 'dopo "Accetta" la mappa si carica');
  await ctx.close();
}

console.log('\n6 · SEO di base');
{
  const ctx = await b.newContext(DESKTOP); const p = await ctx.newPage();
  const titoli = new Set(), descr = new Set();
  for (const path of PAGINE) {
    await p.goto(BASE + path);
    const t = await p.title(); const d = await p.locator('meta[name=description]').getAttribute('content');
    titoli.add(t); descr.add(d);
    const ld = await p.locator('script[type="application/ld+json"]').allTextContents();
    check(ld.some((x) => x.includes('GeneralContractor')) && (await p.locator('h1').count()) === 1, `${path}: dati strutturati e un solo H1`);
  }
  check(titoli.size === PAGINE.length && descr.size === PAGINE.length, 'titoli e descrizioni unici per ogni pagina');
  const sm = await (await fetch(BASE + '/sitemap-0.xml')).text();
  check(PAGINE.filter((x) => x !== '/lavori').every((x) => sm.includes(x === '/' ? '</loc>' : x)), 'sitemap con tutte le pagine');
  const rb = await (await fetch(BASE + '/robots.txt')).text();
  check(rb.includes('Sitemap:'), 'robots.txt con la sitemap');
  await ctx.close();
}

console.log('\n7 · Lingue');
{
  const ctx = await b.newContext(MOBILE);
  const p = await ctx.newPage();
  await p.goto(BASE + '/');
  const bv = p.locator('#bv');
  check(await bv.isVisible(), 'alla prima visita compare la scelta della lingua');
  check((await bv.locator('[data-scegli]').count()) === 5, 'cinque lingue con bandiera', String(await bv.locator('[data-scegli]').count()));
  await bv.locator('[data-scegli=en]').click(); await p.waitForURL('**/en'); await p.waitForLoadState();
  check(await p.evaluate(() => document.documentElement.lang) === 'en', 'scegliendo English si va al sito in inglese');
  check(await p.locator('#bv').isHidden(), 'la scelta viene ricordata (il benvenuto non ricompare)');
  check(await p.locator('header [data-lng] .lng-b').isVisible(), 'nell\'intestazione c\'è il tasto della lingua');
  await p.locator('header [data-lng] .lng-b').click();
  check((await p.locator('header .lng-l a').count()) === 5, 'il tasto apre le cinque lingue');
  await p.goto(BASE + '/ar/muratura');
  check(await p.evaluate(() => document.documentElement.dir) === 'rtl', 'l\'arabo si legge da destra a sinistra');
  check(await p.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), 'in arabo niente scorrimento laterale della pagina');
  const alt = await p.locator('link[rel=alternate][hreflang]').count();
  check(alt === 6, 'ogni pagina indica a Google le sue versioni nelle altre lingue', String(alt));
  await ctx.close();
}

await b.close();
console.log(`\nRisultato: ${ok} superate, ${ko} fallite`);
process.exit(ko ? 1 : 0);
