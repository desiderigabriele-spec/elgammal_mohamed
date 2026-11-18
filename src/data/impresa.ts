// Dati dell'impresa. I campi a null sono DA RICEVERE dal cliente:
// finché sono vuoti, il sito mostra un segnaposto ben visibile.
export const impresa = {
  ragioneSociale: 'EL GAMMAL MOHAMED', // visura camerale: impresa individuale, iscritta il 13/05/2005
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
  telefono: '+39 320 401 6055' as string | null, // chiamate e WhatsApp (niente SMS)
  whatsapp: '393204016055' as string | null, // solo cifre con prefisso
  email: null as string | null,
  piva: '04787430968' as string | null, // visura camerale, Registro Imprese Milano Monza Brianza Lodi
  rea: 'MI-1771917',
  googleBusiness: null as string | null, // link alla scheda Google, quando esiste
  // Indirizzo a cui inviare il modulo (es. Formspree, Web3Forms). Se vuoto, il modulo apre WhatsApp.
  moduloEndpoint: null as string | null,
  zone: ['Sesto San Giovanni', 'Milano', 'Cinisello Balsamo', 'Cologno Monzese', 'Bresso', 'Monza'],
  italia: true, // lavora anche nel resto d'Italia (confermato dall'agenzia)
  estero: ['Germania', 'Francia', 'Paesi arabi'],
};

export const segnaposto = (v: string | null, testo = 'da ricevere') => v ?? `[${testo}]`;

export const telHref = () => (impresa.telefono ? `tel:${impresa.telefono.replace(/\s/g, '')}` : '/contatti');
export const mailHref = (oggetto = 'Richiesta sopralluogo (dal sito)') =>
  impresa.email ? `mailto:${impresa.email}?subject=${encodeURIComponent(oggetto)}` : '/contatti';
export const waHref = (testo = 'Buongiorno, vorrei un sopralluogo gratuito. (dal sito)') =>
  impresa.whatsapp ? `https://wa.me/${impresa.whatsapp}?text=${encodeURIComponent(testo)}` : '/contatti';
