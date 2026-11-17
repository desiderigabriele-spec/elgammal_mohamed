// Dati dell'impresa. I campi a null sono DA RICEVERE dal cliente:
// finché sono vuoti, il sito mostra un segnaposto ben visibile.
export const impresa = {
  ragioneSociale: 'IMPRESA EDILE EL GAMMAL MOHAMED',
  nome: 'El Gammal',
  sottotitolo: 'Impresa edile',
  dal: 2005,
  indirizzo: {
    via: 'Via Guglielmo Marconi 124',
    cap: '20099',
    citta: 'Sesto San Giovanni',
    provincia: 'MI',
    regione: 'Lombardia',
    paese: 'IT',
  },
  // Coordinate indicative del centro di Sesto San Giovanni: da sostituire con quelle esatte della sede
  // quando sarà creata la scheda Google Business.
  geo: { lat: 45.5333, lng: 9.2333 },
  telefono: null as string | null, // es. '+39 333 1234567'
  whatsapp: null as string | null, // solo cifre con prefisso, es. '393331234567'
  email: null as string | null,
  piva: null as string | null,
  googleBusiness: null as string | null, // link alla scheda Google, quando esiste
  // Indirizzo a cui inviare il modulo (es. Formspree, Web3Forms). Se vuoto, il modulo apre WhatsApp.
  moduloEndpoint: null as string | null,
  zone: ['Sesto San Giovanni', 'Milano', 'Cinisello Balsamo', 'Cologno Monzese', 'Bresso', 'Monza'],
  estero: ['Germania', 'Francia', 'Paesi arabi'],
};

export const segnaposto = (v: string | null, testo = 'da ricevere') => v ?? `[${testo}]`;

export const telHref = () => (impresa.telefono ? `tel:${impresa.telefono.replace(/\s/g, '')}` : '/contatti');
export const mailHref = (oggetto = 'Richiesta sopralluogo (dal sito)') =>
  impresa.email ? `mailto:${impresa.email}?subject=${encodeURIComponent(oggetto)}` : '/contatti';
export const waHref = (testo = 'Buongiorno, vorrei un sopralluogo gratuito. (dal sito)') =>
  impresa.whatsapp ? `https://wa.me/${impresa.whatsapp}?text=${encodeURIComponent(testo)}` : '/contatti';
