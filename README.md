# Ordine di Strahler e asta principale in QGIS

Script PyQGIS che, partendo da un reticolo idrografico vettoriale e da un DTM, calcola per ogni tratto l'**ordine di Strahler** e individua l'**asta principale** del bacino.

È lo script usato nel video di **QGIS in Azione** "Dal DTM al reticolo idrografico di un bacino, con QGIS", secondo episodio della mini serie sull'analisi di bacino, realizzata con [Gter](https://www.gter.it/formazione).

Video: https://youtu.be/h-6DBZGXExQ

## Cosa ti serve

- QGIS 3 (nel video: QGIS 3.44 LTR)
- Un **reticolo vettoriale a linee**, per esempio quello estratto con `r.stream.extract` e ritagliato sul bacino. In `r.stream.extract` imposta *v.out.ogr output type* su **line**: con *auto* escono solo i punti
- Il **DTM** da cui hai estratto il reticolo, nello stesso sistema di riferimento

## Come si usa

1. Carica nel progetto il reticolo e il DTM
2. Apri lo script `Strahler.py` e **adatta le due righe con `trova()`** ai nomi dei tuoi layer:
   ```python
   ret = trova('2ha_bacino')   # reticolo
   dem = trova('DTM_terra')    # DTM
   ```
   Basta una parte del nome, senza distinzione tra maiuscole e minuscole, purché individui un solo layer. Se ne trova zero o più di uno, lo script si ferma e ti elenca i nomi dei layer presenti nel progetto
3. Nel menu Plugins apri la **Python Console**, poi l'editor (icona *Show Editor*), apri il file e lancialo con *Run Script*
4. Nella console compare una riga con la quota dello sbocco, l'ordine massimo e la lunghezza dell'asta principale

## Cosa fa

- **Sbocco**: tra le estremità libere del reticolo sceglie quella con la quota più bassa sul DTM
- **Ordine di Strahler**: risale il reticolo dallo sbocco. I tratti di testata hanno ordine 1; a una confluenza l'ordine aumenta di 1 solo se si incontrano due rami dello stesso ordine massimo, altrimenti resta quello del ramo maggiore
- **Asta principale**: dallo sbocco risale e a ogni confluenza segue il ramo con il percorso più lungo fino alla testata. Per questo l'asta non coincide con i soli tratti di ordine massimo, che ne coprono solo la parte bassa

Al layer del reticolo vengono aggiunti due campi:

| Campo | Contenuto |
|---|---|
| `strahler` | ordine di Strahler del tratto |
| `asta_princ` | 1 se il tratto fa parte dell'asta principale, 0 altrimenti |

Per avere l'asta come una sola linea: seleziona i tratti con `asta_princ = 1` e usa **Dissolve** con *Selected features only*.

## Limiti

- Lo script **modifica il layer** aggiungendo i due campi: se vuoi conservare l'originale, lavora su una copia
- Il reticolo deve essere **connesso e ad albero**, con le estremità dei tratti coincidenti nelle confluenze (lo script le confronta arrotondate al centimetro). Tratti staccati restano senza ordine; un reticolo con anelli non viene gestito
- Il risultato dipende dal reticolo che gli dai: il DTM non vede i tombini, e dove il torrente passa sotto un rilevato stradale il reticolo calcolato devia e va corretto prima

## Contatti

Paolo Corradeghini, 3DMetrica
- YouTube: canale di 3DMetrica
- LinkedIn: [linkedin.com/in/paolocorradeghini](https://www.linkedin.com/in/paolocorradeghini)
- Gruppo Telegram di QGIS in Azione: [t.me/+ZKm37iQHD083MTRk](https://t.me/+ZKm37iQHD083MTRk)
