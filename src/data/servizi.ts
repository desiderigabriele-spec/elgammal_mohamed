import type { ImageMetadata } from 'astro';
import muratura from '../assets/servizi/muratura.webp';
import imbianchino from '../assets/servizi/intonaci.webp';
import rasato from '../assets/servizi/rasatura.webp';
import impianti from '../assets/servizi/impianti.webp';
import controsoffitto from '../assets/servizi/cartongesso.webp';
import facciata from '../assets/servizi/facciate.webp';
import soggiorno from '../assets/servizi/chiavi-in-mano.webp';

export interface Servizio {
  slug: string;
  num: string; // numero dello strato
  nome: string;
  breve: string;
  title: string; // <title>
  description: string; // meta description
  h1: string;
  spessore: string; // quota mostrata nel disegno
  foto: ImageMetadata;
  fotoAlt: string;
  fotoNota?: string; // scritta sotto la foto (predefinita: "Foto di esempio")
  intro: string;
  problema: { titolo: string; testo: string; segni: string[] };
  soluzione: { titolo: string; testo: string; include: string[] };
  passi: { t: string; d: string }[];
  nota?: string; // segnaposto da confermare col cliente
  prova?: { titolo: string; passi: string[] };
  faq: { q: string; a: string }[];
}

const passiBase = (lavoro: string, consegna: string) => [
  { t: 'Sopralluogo gratuito', d: 'Veniamo a vedere, misuriamo e ascoltiamo cosa ti serve.' },
  { t: 'Preventivo gratuito', d: 'Scritto voce per voce, così sai cosa è compreso.' },
  { t: 'Lavoro', d: lavoro },
  { t: 'Consegna', d: consegna },
];

const faqGratis = {
  q: 'Il sopralluogo e il preventivo si pagano?',
  a: 'No. Sopralluogo e preventivo sono gratuiti e non ti impegnano a nulla.',
};
const faqPiccoli = (cosa: string) => ({
  q: `Fate anche lavori piccoli, ${cosa}?`,
  a: 'Sì. Non c\'è un importo minimo: valutiamo lavori di qualsiasi dimensione.',
});

export const servizi: Servizio[] = [
  {
    slug: 'muratura',
    num: '01',
    nome: 'Muratura',
    breve: 'Pareti nuove, tramezzi, aperture e chiusure. Lo strato che regge tutti gli altri.',
    title: 'Muratura e opere murarie a Sesto San Giovanni e Milano | El Gammal',
    description:
      'Muratore a Sesto San Giovanni e Milano: tramezzi, pareti nuove, aperture e chiusure di vani, ripristino di murature. Sopralluogo e preventivo gratuiti.',
    h1: 'Muratura a Sesto San Giovanni e Milano',
    spessore: '8–30 cm',
    foto: muratura,
    fotoAlt: 'Tramezzo nuovo in blocchi di laterizio con l\'apertura per la porta',
    fotoNota: 'Immagine illustrativa',
    intro:
      'Pareti nuove, tramezzi, aperture e chiusure. È lo strato che regge tutti gli altri: se il muro è dritto, intonaco, rasatura e pittura vengono meglio e durano di più.',
    problema: {
      titolo: 'Un muro storto si paga due volte',
      testo:
        'Quando una parete è fuori piombo o un\'apertura è fatta male, ogni strato sopra deve correggere l\'errore: più intonaco, più stucco, crepe che tornano.',
      segni: [
        'Crepe che si riaprono dopo ogni imbiancatura',
        'Porte e finestre che non chiudono bene',
        'Pareti storte che si notano con la luce di lato',
        'Stanze da ridistribuire o da dividere',
      ],
    },
    soluzione: {
      titolo: 'Costruiamo la base giusta',
      testo:
        'Partiamo dal muro, a piombo e in squadra. Poi, se serve, facciamo noi anche tutti gli strati sopra: un\'impresa sola dal primo mattone al colore.',
      include: [
        'Tramezzi e pareti divisorie in laterizio o blocchi',
        'Apertura e chiusura di porte e vani',
        'Ripristino di murature danneggiate',
        'Tracce e chiusure per il passaggio degli impianti',
        'Anche una sola parete',
      ],
    },
    passi: passiBase(
      'Costruiamo a piombo e in squadra, con un referente che risponde per tutto il cantiere.',
      'Controlliamo insieme il muro finito, pronto per intonaco e rasatura.',
    ),
    faq: [
      faqPiccoli('come una sola parete'),
      {
        q: 'Quanto tempo serve per costruire un tramezzo?',
        a: 'Dipende da misure, materiale e accesso al cantiere. Al sopralluogo ti diciamo i tempi per il tuo caso.',
      },
      {
        q: 'Dopo la muratura fate anche intonaco e rasatura?',
        a: 'Sì. È il vantaggio di un\'impresa sola: lo stesso referente segue tutti gli strati, dal muro alla pittura.',
      },
      faqGratis,
    ],
  },
  {
    slug: 'intonaci-imbiancatura',
    num: '02',
    nome: 'Intonaci, imbiancatura e sottofondi',
    breve: 'Il primo strato di finitura, l\'ultima mano di colore e i sottofondi per i pavimenti.',
    title: 'Intonaci, imbiancatura e sottofondi a Sesto San Giovanni | El Gammal',
    description:
      'Intonaci interni ed esterni, imbiancatura di case, scale e androni, sottofondi per pavimenti a Sesto San Giovanni e Milano. Sopralluogo e preventivo gratuiti.',
    h1: 'Intonaci e imbiancatura a Sesto San Giovanni e Milano',
    spessore: '1,5–2 cm',
    foto: imbianchino,
    fotoAlt: 'Parete con l\'intonaco grigio e la prima mano di bianco, scala e rullo',
    fotoNota: 'Immagine illustrativa',
    intro:
      'L\'intonaco prepara il muro, la pittura lo finisce, il sottofondo prepara il pavimento. Sono gli strati che si vedono di più: devono essere fatti bene.',
    problema: {
      titolo: 'Pittura che si sfoglia, intonaco che si stacca',
      testo:
        'Quasi sempre il problema non è la pittura, ma quello che c\'è sotto: un fondo non preparato, umidità, un intonaco che non tiene più.',
      segni: [
        'Pittura che fa bolle o si sfoglia',
        'Intonaco che suona vuoto o si stacca',
        'Aloni e macchie che tornano',
        'Pavimenti da posare su un fondo irregolare',
      ],
    },
    soluzione: {
      titolo: 'Prima il fondo, poi il colore',
      testo:
        'Controlliamo cosa c\'è sotto, ripristiniamo l\'intonaco dove serve e solo dopo pitturiamo. Così il colore dura.',
      include: [
        'Intonaci interni ed esterni',
        'Ripristino di intonaci che si staccano',
        'Imbiancatura di stanze, scale e androni',
        'Sottofondi per pavimenti',
        'Anche una sola stanza',
      ],
    },
    passi: passiBase(
      'Proteggiamo quello che resta nella stanza, prepariamo il fondo e poi diamo il colore.',
      'Riconsegniamo gli ambienti in ordine, pronti da vivere.',
    ),
    faq: [
      faqPiccoli('come una sola stanza'),
      {
        q: 'Che differenza c\'è tra intonaco e rasatura?',
        a: 'L\'intonaco è lo strato più spesso, in genere 1,5–2 cm, e regolarizza il muro. La rasatura è di pochi millimetri e rende la superficie liscia, pronta per la pittura.',
      },
      {
        q: 'Lavorate anche su scale e parti comuni dei condomini?',
        a: 'Sì, lavoriamo per privati, condomini e aziende.',
      },
      faqGratis,
    ],
  },
  {
    slug: 'rasatura-pareti',
    num: '03',
    nome: 'Rasatura e lisciatura',
    breve: 'Pochi millimetri che fanno la differenza: pareti e soffitti lisci, dentro e fuori.',
    title: 'Rasatura pareti a Sesto San Giovanni e Milano | El Gammal',
    description:
      'Rasatura e lisciatura di pareti e soffitti, interni ed esterni, a Sesto San Giovanni e Milano. Superfici lisce anche alla luce radente. Preventivo gratuito.',
    h1: 'Rasatura pareti a Sesto San Giovanni e Milano',
    spessore: '2–3 mm',
    foto: rasato,
    fotoAlt: 'Parete rasata a stucco con spatole e lampada da cantiere',
    fotoNota: 'Immagine illustrativa',
    intro:
      'Pochi millimetri che fanno la differenza: pareti e soffitti lisci, senza onde e senza giunte che si vedono. Dentro e fuori casa.',
    problema: {
      titolo: 'Onde, buchi e giunte che si vedono',
      testo:
        'Di giorno sembra tutto a posto. Poi la sera, con una lampada di lato, la parete si riempie di ombre: sono i difetti della superficie.',
      segni: [
        'Ombre e onde con la luce di lato',
        'Segni di vecchi stucchi e riparazioni',
        'Pareti ruvide dopo aver tolto la carta da parati',
        'Giunte del cartongesso che si vedono',
      ],
    },
    soluzione: {
      titolo: 'Superfici lisce, anche alla luce radente',
      testo:
        'Stendiamo la rasatura a strati sottili e la lisciamo fino ad avere una superficie uniforme, pronta per la pittura.',
      include: [
        'Rasatura di pareti e soffitti interni',
        'Rasatura esterna',
        'Lisciatura per finiture lisce',
        'Rasatura dopo la rimozione della carta da parati',
        'Preparazione delle superfici per la pittura',
      ],
    },
    prova: {
      titolo: 'La prova della torcia: come capire se un muro è fatto bene',
      passi: [
        'Spegni la luce della stanza, meglio di sera.',
        'Appoggia una torcia al muro, quasi parallela alla parete.',
        'Guarda le ombre: ogni ombra è un\'onda, un buco o una giunta. Un muro ben rasato resta uniforme.',
      ],
    },
    passi: passiBase(
      'Proteggiamo pavimenti e infissi, rasiamo a strati sottili e controlliamo la superficie con la luce di lato.',
      'Controlliamo insieme il lavoro finito: puoi fare anche tu la prova della torcia.',
    ),
    faq: [
      {
        q: 'Come capisco se una rasatura è fatta bene?',
        a: 'Con la prova della torcia: al buio, appoggia una torcia al muro quasi parallela alla parete. Se non vedi ombre, la superficie è uniforme.',
      },
      {
        q: 'Si può rasare sopra la pittura vecchia?',
        a: 'Dipende da com\'è la pittura: se è ben attaccata, spesso sì, dopo una preparazione. Se si sfoglia va tolta prima. Lo vediamo al sopralluogo.',
      },
      {
        q: 'Quanto è spessa una rasatura?',
        a: 'In genere pochi millimetri. Serve a rendere liscia la superficie, non a correggere muri molto storti: per quelli si interviene prima con l\'intonaco.',
      },
      {
        q: 'Fate la rasatura anche all\'esterno?',
        a: 'Sì, facciamo rasature sia interne sia esterne, anche sulle facciate.',
      },
      faqGratis,
    ],
  },
  {
    slug: 'cartongesso',
    num: '04',
    nome: 'Cartongesso',
    breve: 'Pareti, contropareti, controsoffitti, nicchie e velette. Veloce e pulito.',
    title: 'Cartongesso a Sesto San Giovanni e Milano: pareti e controsoffitti | El Gammal',
    description:
      'Pareti divisorie, contropareti e controsoffitti in cartongesso a Sesto San Giovanni e Milano, per case, uffici e negozi. Sopralluogo e preventivo gratuiti.',
    h1: 'Cartongesso a Sesto San Giovanni e Milano',
    spessore: 'lastra 12,5 mm',
    foto: controsoffitto,
    fotoAlt: 'Controparete e controsoffitto in cartongesso con i profili metallici',
    fotoNota: 'Immagine illustrativa',
    intro:
      'Pareti nuove, contropareti, controsoffitti con luci incassate, nicchie e velette. Il cartongesso cambia una stanza in pochi giorni e con poca polvere.',
    problema: {
      titolo: 'Spazi che non funzionano più',
      testo:
        'Una stanza da dividere, un impianto da nascondere, un soffitto troppo alto o luci da cambiare. Con la muratura servirebbe più tempo.',
      segni: [
        'Una stanza grande da dividere in due',
        'Tubi e cavi a vista da nascondere',
        'Luci da incassare nel soffitto',
        'Un ufficio da riorganizzare',
      ],
    },
    soluzione: {
      titolo: 'Strutture leggere, finiture da muro vero',
      testo:
        'Montiamo la struttura, chiudiamo con le lastre, stucchiamo e rasiamo i giunti. Alla fine non si distingue da un muro tradizionale.',
      include: [
        'Pareti divisorie',
        'Contropareti, anche per far passare gli impianti',
        'Controsoffitti, anche con luci incassate',
        'Nicchie, velette e librerie',
        'Lavori per uffici e negozi',
      ],
    },
    passi: passiBase(
      'Montiamo struttura e lastre, poi stucchiamo e rasiamo i giunti finché non si vedono più.',
      'Consegniamo superfici pronte da pitturare, o già pitturate se lo chiedi.',
    ),
    faq: [
      {
        q: 'Cartongesso o muratura: cosa conviene?',
        a: 'Il cartongesso è più leggero e veloce e fa passare facilmente gli impianti. La muratura è più massiccia. Facciamo tutte e due, quindi ti consigliamo quella giusta per il tuo caso.',
      },
      {
        q: 'Si possono appendere mensole e pensili al cartongesso?',
        a: 'Sì, se la parete è preparata nei punti giusti con i rinforzi. Dicci prima cosa vuoi appendere e lo prevediamo.',
      },
      {
        q: 'Fate controsoffitti con faretti?',
        a: 'Sì, anche con luci incassate, coordinando i passaggi degli impianti nello stesso cantiere.',
      },
      faqPiccoli('come una nicchia o una veletta'),
      faqGratis,
    ],
  },
  {
    slug: 'impianti',
    num: '05',
    nome: 'Impianti',
    breve: 'Coordinati con le opere murarie, nello stesso cantiere.',
    title: 'Impianti nelle ristrutturazioni a Sesto San Giovanni e Milano | El Gammal',
    description:
      'Impianti coordinati con le opere murarie nelle ristrutturazioni a Sesto San Giovanni e Milano: tracce, passaggi e rifacimento impianti. Preventivo gratuito.',
    h1: 'Impianti nelle ristrutturazioni a Sesto San Giovanni e Milano',
    spessore: 'dietro le pareti',
    foto: impianti,
    fotoAlt: 'Muro con le tracce aperte, tubi per acqua ed elettricità e scatole incassate',
    fotoNota: 'Immagine illustrativa',
    intro:
      'Gli impianti stanno dentro i muri: per questo vanno fatti insieme alle opere murarie, nello stesso cantiere e con lo stesso referente.',
    problema: {
      titolo: 'Muri aperti due volte',
      testo:
        'Quando muratore e impiantista non si parlano, si rompe un muro appena finito per far passare un tubo. Tempo perso e polvere in più.',
      segni: [
        'Impianti vecchi da rifare durante la ristrutturazione',
        'Prese e punti luce da spostare',
        'Bagno o cucina da ridisegnare',
        'Tracce da aprire e richiudere',
      ],
    },
    soluzione: {
      titolo: 'Un ordine di lavoro solo',
      testo:
        'Organizziamo tracce, passaggi e chiusure insieme agli impianti, così ogni muro si apre una volta sola e si chiude subito dopo.',
      include: [
        'Tracce, passaggi e chiusure',
        'Impianti elettrici',
        'Impianti idraulici, bagni e cucine',
        'Coordinamento con le opere murarie e le finiture',
      ],
    },
    nota: 'Da confermare con il cliente: quali impianti esegue direttamente e con quali abilitazioni.',
    passi: passiBase(
      'Apriamo le tracce, facciamo passare gli impianti e richiudiamo, nell\'ordine giusto.',
      'Muri chiusi e pronti per intonaco, rasatura e pittura.',
    ),
    faq: [
      {
        q: 'Perché conviene fare impianti e muratura con la stessa impresa?',
        a: 'Perché ogni muro si apre e si chiude una volta sola, nell\'ordine giusto, e c\'è un solo referente per tutto.',
      },
      faqPiccoli('come spostare una presa'),
      faqGratis,
    ],
  },
  {
    slug: 'facciate',
    num: '06',
    nome: 'Facciate',
    breve: 'Ripristino e rifacimento per case e condomini.',
    title: 'Rifacimento facciate a Sesto San Giovanni e Milano | El Gammal',
    description:
      'Rifacimento e ripristino di facciate per case e condomini a Sesto San Giovanni e Milano: intonaci, rasature, tinteggiatura esterna. Preventivo chiaro per l\'assemblea.',
    h1: 'Rifacimento facciate a Sesto San Giovanni e Milano',
    spessore: 'lato esterno',
    foto: facciata,
    fotoAlt: 'Facciata di condominio: una parte rifatta color sabbia, una parte rovinata e una col ponteggio',
    fotoNota: 'Immagine illustrativa',
    intro:
      'La facciata è il lato che vede tutto il quartiere. Ripristiniamo intonaci, rasiamo e tinteggiamo, per case singole e condomini.',
    problema: {
      titolo: 'Intonaco che si stacca: non è solo estetica',
      testo:
        'Un pezzo di intonaco che cade da un balcone o da un cornicione è un pericolo per chi passa sotto. Prima si interviene, meno lavoro serve.',
      segni: [
        'Intonaco che si gonfia o si stacca',
        'Crepe e macchie di umidità',
        'Frontalini dei balconi rovinati',
        'Colore sbiadito e sporco',
      ],
    },
    soluzione: {
      titolo: 'Dal ripristino alla tinteggiatura',
      testo:
        'Togliamo l\'intonaco che non tiene, ripristiniamo, rasiamo e finiamo con la tinteggiatura esterna. Per gli amministratori, un preventivo chiaro da portare in assemblea.',
      include: [
        'Ripristino di intonaci esterni',
        'Rasatura e finitura della facciata',
        'Tinteggiatura esterna',
        'Ripristino di balconi e frontalini',
        'Case singole e condomini',
      ],
    },
    passi: passiBase(
      'Organizziamo il cantiere per dare il meno fastidio possibile, con un referente unico per amministratore e condomini.',
      'Controlliamo insieme la facciata finita.',
    ),
    faq: [
      {
        q: 'Fate preventivi da portare in assemblea di condominio?',
        a: 'Sì: un preventivo scritto voce per voce, chiaro da confrontare con gli altri.',
      },
      {
        q: 'Quando conviene programmare i lavori in facciata?',
        a: 'I lavori esterni si fanno meglio con tempo stabile e asciutto. Conviene chiedere il sopralluogo per tempo, così il preventivo è pronto quando serve all\'assemblea.',
      },
      {
        q: 'Chi parla con i condomini durante i lavori?',
        a: 'Un referente unico, che tiene i contatti con l\'amministratore per tutta la durata del cantiere.',
      },
      {
        q: 'L\'impresa è assicurata?',
        a: 'Sì. L\'impresa è assicurata e il personale è formato sulla sicurezza.',
      },
      faqGratis,
    ],
  },
  {
    slug: 'ristrutturazioni-chiavi-in-mano',
    num: '=',
    nome: 'Ristrutturazioni chiavi in mano',
    breve: 'Tutti gli strati, un solo referente. Dal primo mattone all\'ultima mano di colore.',
    title: 'Ristrutturazioni chiavi in mano a Sesto San Giovanni e Milano | El Gammal',
    description:
      'Ristrutturazione chiavi in mano di appartamenti, case, uffici e negozi a Sesto San Giovanni e Milano. Un\'impresa sola, un referente. Sopralluogo gratuito.',
    h1: 'Ristrutturazioni chiavi in mano a Sesto San Giovanni e Milano',
    spessore: 'tutti gli strati',
    foto: soggiorno,
    fotoAlt: 'Stanza appena ristrutturata: pareti bianche, parquet in rovere, controsoffitto con faretti',
    fotoNota: 'Immagine illustrativa',
    intro:
      'Muratura, impianti, intonaci, rasature, cartongesso e pittura: tutti gli strati della tua casa con un\'impresa sola e un referente solo.',
    problema: {
      titolo: 'Cinque artigiani, nessun responsabile',
      testo:
        'Quando ogni lavoro è affidato a qualcuno di diverso, i ritardi di uno bloccano tutti gli altri e nessuno risponde del risultato.',
      segni: [
        'Paura che i lavori non finiscano mai',
        'Artigiani diversi da coordinare',
        'Non sapere chi chiamare quando c\'è un problema',
        'Sorprese a metà lavoro',
      ],
    },
    soluzione: {
      titolo: 'Un\'impresa sola, dall\'inizio alla fine',
      testo:
        'Facciamo noi tutti i lavori edili del cantiere, nell\'ordine giusto. Nel preventivo trovi l\'elenco preciso di cosa è compreso: chiavi in mano, ma scritto.',
      include: [
        'Demolizioni e muratura',
        'Impianti coordinati con le opere murarie',
        'Intonaci, rasature e cartongesso',
        'Pittura e finiture',
        'Appartamenti, case, uffici e negozi',
      ],
    },
    passi: passiBase(
      'Seguiamo tutti gli strati nell\'ordine giusto, con un referente che risponde per tutto.',
      'Controlliamo insieme il lavoro finito e ti consegniamo le chiavi.',
    ),
    faq: [
      {
        q: 'Cosa vuol dire "chiavi in mano"?',
        a: 'Che ci occupiamo di tutti i lavori edili del cantiere, con un solo referente. Nel preventivo trovi l\'elenco preciso di cosa è compreso, così non ci sono dubbi.',
      },
      {
        q: 'Posso ristrutturare solo una parte della casa?',
        a: 'Sì. Anche solo un bagno o una stanza: non c\'è un importo minimo.',
      },
      {
        q: 'Lavorate anche fuori Milano?',
        a: 'Lavoriamo ogni giorno a Milano e nell\'hinterland, e abbiamo già lavorato anche in Germania, in Francia e nei Paesi arabi.',
      },
      faqGratis,
    ],
  },
];

export const servizioPerSlug = (s: string) => servizi.find((x) => x.slug === s);
