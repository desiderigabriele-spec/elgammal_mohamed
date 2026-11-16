# Video "Dalla casa vecchia alla casa tua" · Prompt

## L'idea
Come nel video di esempio, ma con una **ristrutturazione** invece di una costruzione nuova.
Una sola stanza di un appartamento milanese degli anni '60, **inquadratura sempre ferma**.
Mentre il visitatore scorre la home, la stanza si trasforma fase dopo fase, e ogni fase è uno dei servizi di El Gammal:

| Fase | Titolo sul sito | Servizio |
|---|---|---|
| 0 | Il sopralluogo | – |
| 1 | Si comincia | Ristrutturazione chiavi in mano |
| 2 | La muratura | 01 Muratura |
| 3 | Gli impianti | 05 Impianti |
| 4 | Gli intonaci | 02 Intonaci |
| 5 | Il cartongesso | 04 Cartongesso |
| 6 | La rasatura | 03 Rasatura |
| 7 | Casa tua | Pittura e consegna |

Alla fine compare la frase: **"Dal primo mattone all'ultima mano di colore."**

## Come si fa (3 passi)
1. **8 immagini chiave** (le fasi 0–7), tutte con la stessa inquadratura. Si fanno con ChatGPT, nella **stessa chat**, ritoccando ogni volta l'ultima immagine.
2. **7 video di passaggio**, uno tra ogni coppia di immagini (0→1, 1→2, … 6→7). Servono strumenti video che accettano **immagine iniziale e immagine finale**, per esempio Kling, Runway, Luma o Google Veo/Flow. ChatGPT da solo non lo fa in modo affidabile.
3. Mi mandi i 7 video (o uno solo già unito). Io li trasformo in fotogrammi leggeri e costruisco l'effetto sul sito, veloce anche sul telefono.

Formato: **orizzontale 16:9**. Tieni **la finestra e la parete principale al centro**: sul telefono mostro la parte centrale dell'immagine.

---

## PASSO 1 · Le 8 immagini chiave (ChatGPT, stessa chat)

### Stile comune (incollare per primo)
```
Per tutte le immagini di questa chat:
fotografia realistica di interni, reflex con obiettivo 24 mm, cavalletto fisso, formato orizzontale 16:9 (1536x864 o il più vicino possibile).
La stessa stanza vista sempre dalla stessa identica posizione: una stanza rettangolare di un appartamento milanese degli anni '60,
una grande finestra al centro della parete di fondo con vista su tetti e cielo di città (nessun edificio riconoscibile),
parete di fondo e soffitto ben visibili, pavimento visibile.
Nessun testo, nessun logo, nessun marchio, nessuna persona.
Massimo realismo nei materiali: mattoni, malta, intonaco, gesso, pittura, legno.
Mantieni sempre identici inquadratura, prospettiva, posizione e forma della finestra e dimensioni della stanza: cambia solo quello che ti chiedo.
```

### fase-0-sopralluogo.png
```
La stanza com'è oggi, vecchia e trascurata: carta da parati sbiadita e strappata in alcuni punti, intonaco con crepe e macchie di umidità vicino al soffitto,
pavimento in graniglia consumata, vecchi termosifoni in ghisa, luce grigia del mattino. Stanza vuota, nessun mobile.
```

### fase-1-si-comincia.png
```
Modifica l'ultima immagine. Inquadratura identica.
La stanza è stata svuotata e preparata: carta da parati tolta, intonaco rovinato rimosso fino ai mattoni in alcune zone,
pavimento coperto da un telo protettivo pulito, sacchi di macerie chiusi e ordinati in un angolo. Luce del mattino.
```

### fase-2-muratura.png
```
Modifica l'ultima immagine. Inquadratura identica.
Sul lato destro della stanza è stato costruito un nuovo tramezzo in mattoni forati rossi, perfettamente a piombo, con un vano porta.
Malta pulita nei giunti. Il resto della stanza come prima.
```

### fase-3-impianti.png
```
Modifica l'ultima immagine. Inquadratura identica.
Sulle pareti ci sono tracce aperte, dritte e ordinate, con tubi corrugati grigi e scatole elettriche murate; sotto la finestra i tubi per il nuovo termosifone.
I vecchi termosifoni in ghisa sono stati tolti.
```

### fase-4-intonaci.png
```
Modifica l'ultima immagine. Inquadratura identica.
Tutte le pareti, compreso il nuovo tramezzo, sono intonacate con intonaco grigio grezzo uniforme; le tracce degli impianti sono chiuse.
```

### fase-5-cartongesso.png
```
Modifica l'ultima immagine. Inquadratura identica.
Al soffitto è stato montato un controsoffitto in cartongesso con una veletta lungo la parete di fondo e i fori per i faretti incassati.
Giunti delle lastre stuccati. Pareti ancora grigie.
```

### fase-6-rasatura.png
```
Modifica l'ultima immagine. Inquadratura identica.
Pareti e controsoffitto sono rasati: superfici bianche perfettamente lisce, senza onde. Una luce radente dal lato della finestra mostra che le pareti sono perfette.
Pavimento ancora coperto dal telo.
```

### fase-7-casa-tua.png
```
Modifica l'ultima immagine. Inquadratura identica.
Lavoro finito: pareti pitturate in bianco caldo, nuovo pavimento in parquet di rovere chiaro, termosifone moderno sotto la finestra, faretti accesi nel controsoffitto.
La stanza è arredata come un soggiorno elegante e sobrio: divano chiaro, tappeto, una pianta, una lampada da terra.
Luce calda del tramonto che entra dalla finestra, cielo arancio e viola sopra i tetti. Atmosfera accogliente.
```

---

## PASSO 2 · I 7 video di passaggio (Kling, Runway, Luma o Veo)

Impostazioni per ogni video:
- **Immagine iniziale** = fase N, **immagine finale** = fase N+1
- Durata **4–5 secondi**, formato **16:9**, risoluzione **1080p**, **senza audio**
- Movimento di camera: **nessuno** (camera bloccata)

Prompt da usare per tutti (cambia solo la parte tra parentesi quadre):
```
Timelapse realistico di un cantiere di ristrutturazione, camera completamente ferma su cavalletto, nessun movimento di camera, nessuno zoom.
[DESCRIZIONE DEL PASSAGGIO].
I materiali compaiono in modo progressivo e credibile, come in un vero timelapse. Nessuna persona visibile, nessun testo.
La luce cambia piano e in modo naturale.
```

Descrizioni da inserire:
- **0 → 1:** la carta da parati e l'intonaco rovinato vengono tolti, il pavimento viene coperto da un telo, i sacchi di macerie si allineano nell'angolo
- **1 → 2:** il nuovo tramezzo in mattoni si alza fila dopo fila, dal pavimento verso l'alto
- **2 → 3:** si aprono le tracce nei muri e compaiono i tubi e le scatole elettriche; i vecchi termosifoni spariscono
- **3 → 4:** l'intonaco grigio copre le pareti da un lato all'altro, chiudendo le tracce
- **4 → 5:** i profili metallici e le lastre del controsoffitto vengono montati, poi i giunti vengono stuccati
- **5 → 6:** la rasatura bianca si stende sulle pareti e sul soffitto, che diventano lisci
- **6 → 7:** le pareti si colorano, il parquet si posa, arrivano gli arredi e la luce diventa quella calda del tramonto

Se un video "inventa" troppo (cambia la stanza, muove la camera), rifallo: conta che inizio e fine combacino con le immagini.

---

## PASSO 3 · Cosa mandarmi
- I **7 video** in MP4 (fase-0-1.mp4 … fase-6-7.mp4), oppure uno unico già montato.
- Le **8 immagini chiave** in PNG.

Io:
- ricavo circa 150–200 fotogrammi leggeri in WebP/AVIF (una versione grande per il computer e una piccola per il telefono);
- costruisco la sezione: l'immagine resta ferma sullo schermo e cambia mentre scorri, con il titolo della fase, il numero dello strato e un contatore;
- carico subito solo il primo fotogramma e gli altri dopo, così il sito resta veloce (obiettivo PageSpeed sopra 90 sul telefono);
- se il telefono chiede "riduci movimento", mostro le 8 immagini chiave una sotto l'altra, senza animazione.

## Nota
Sono immagini illustrative del metodo di lavoro, non un cantiere vero di El Gammal: vicino all'animazione scriviamo una riga piccola, "Ricostruzione illustrativa".
Se in futuro il cliente filma un suo cantiere con il telefono su cavalletto, possiamo fare la stessa cosa con un lavoro vero: sarebbe ancora più forte.
