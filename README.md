# Python Socket Examples — TCP & UDP

Una raccolta di script didattici che mostrano come funziona la comunicazione di rete a livello di socket in Python. Gli esempi implementano un semplice protocollo **ping-pong**: il client invia `"PING"`, il server risponde `"PONG"`.

La repository contiene inoltre le soluzioni a quattro esercizi che estendono progressivamente gli esempi base, esplorando refactoring, server con stato, gestione multi-client, simulazione di perdita di pacchetti e progettazione di protocolli custom.

---

## Struttura della Repository

```
python-socket-examples/
├── README.md
├── exercise_0/
│   ├── tcp_server.py
│   ├── tcp_client.py
│   ├── udp_server.py
│   └── udp_client.py
├── exercise_1/
│   ├── udp_server.py
│   └── udp_client.py
├── exercise_2/
│   ├── tcp_server_sequential.py
│   ├── tcp_server_threaded.py
│   └── tcp_client.py
├── exercise_3/
│   ├── udp_server.py
│   └── udp_client.py
└── exercise_4/
    ├── calc_server.py
    └── calc_client.py
```

---

## Requisiti

- Python **3.6** o versione successiva
- Nessuna dipendenza esterna — solo libreria standard (`socket`, `time`, `threading`, `random`)

---

## Come Eseguire

Ogni esempio richiede **due terminali aperti contemporaneamente**: uno per il server e uno per il client. **Avviare sempre prima il server.**

### Esempi originali

```bash
# TCP
python original/tcp_server.py
python original/tcp_client.py

# UDP
python original/udp_server.py
python original/udp_client.py
```

### Esercizio 0 — Codice refactored

```bash
python exercise_0/tcp_server.py
python exercise_0/tcp_client.py

python exercise_0/udp_server.py
python exercise_0/udp_client.py
```

### Esercizio 1 — Contatore messaggi

```bash
python exercise_1/udp_server.py
python exercise_1/udp_client.py
```

Output atteso (lato client):
```
[Client] Reply from ('127.0.0.1', 65433): 'PONG #1'
[Client] Reply from ('127.0.0.1', 65433): 'PONG #2'
...
```

### Esercizio 2 — Server TCP multi-client

**Sequenziale** (serve i client uno alla volta, fino a `MAX_CLIENTS`):
```bash
python exercise_2/tcp_server_sequential.py
python exercise_2/tcp_client.py   # eseguire più volte
```

**Con thread** (gestisce più client contemporaneamente):
```bash
python exercise_2/tcp_server_threaded.py
python exercise_2/tcp_client.py   # aprire più terminali ed eseguire in parallelo
```

### Esercizio 3 — Simulazione canale inaffidabile

```bash
python exercise_3/udp_server.py
python exercise_3/udp_client.py
```

Il server scarta casualmente circa il 30% delle risposte. Il client gestisce i timeout e stampa un riepilogo finale:
```
[Client] Done. Received 7/10 replies.
```
Per modificare la probabilità di perdita, cambiare `DROP_PROBABILITY` in `exercise_3/udp_server.py`.

### Esercizio 4 — Calcolatrice (protocollo TCP custom)

```bash
python exercise_4/calc_server.py
python exercise_4/calc_client.py
```

Esempio di sessione interattiva:
```
>>> 3 + 4
    RESULT: 7
>>> 2 ** 10
    RESULT: 1024
>>> 10 / 0
    ERROR: Division by zero
>>> sqrt(9)
    ERROR: name 'sqrt' is not defined
>>> quit
    BYE
```

---

## TCP vs UDP — Differenze Principali

| | TCP (`SOCK_STREAM`) | UDP (`SOCK_DGRAM`) |
|---|---|---|
| Connessione | Three-way handshake obbligatorio | Nessuna — fire and forget |
| Setup server | `bind` → `listen` → `accept` | Solo `bind` |
| Setup client | `connect` | Nessuno |
| Invio | `sendall(data)` | `sendto(data, indirizzo)` |
| Ricezione | `recv(n)` | `recvfrom(n)` → restituisce dati + indirizzo mittente |
| Garanzia di consegna | Sì — TCP ritrasmette i pacchetti persi | No — i datagrammi possono essere persi o riordinati |
| Chiusura | `close()` invia FIN/ACK | `close()` rilascia solo il file descriptor locale |
| Casi d'uso tipici | HTTP, SSH, database | DNS, streaming video, giochi online |

---

## Spiegazione del Codice

### Esercizio 0 — Refactoring

Rispetto al codice originale sono state introdotte le seguenti modifiche su tutti e quattro i file:

- **Funzioni dedicate**: la logica è suddivisa in funzioni con responsabilità singola. `create_server_socket()` / `create_udp_socket()` si occupano esclusivamente della configurazione del socket; `handle_message()` / `build_reply()` contengono la logica applicativa PING → PONG; `serve_client()` / `receive_and_reply()` gestiscono il ciclo di comunicazione.
- **Context manager `with`**: i socket vengono aperti con `with socket.socket(...) as sock`, che garantisce la chiusura automatica anche in caso di eccezione, eliminando la necessità di blocchi `try/finally` espliciti.
- **Costanti in `UPPER_CASE`**: valori configurabili come `HOST`, `PORT`, `BUFFER_SIZE`, `NUM_PINGS` sono dichiarati come costanti a livello di modulo secondo la convenzione PEP 8, rendendo immediata la loro identificazione e modifica.

### Esercizio 1 — Contatore messaggi

- **`ping_count`**: variabile intera locale alla funzione `main()` del server. Viene incrementata ogni volta che il server riceve un messaggio `"PING"` e inclusa nella risposta tramite `build_reply()`, producendo stringhe come `"PONG #1"`, `"PONG #2"` ecc.
- **Persistenza**: il contatore sopravvive per tutta la durata del processo server. Se il server viene riavviato, il contatore riparte da zero perché la variabile è in memoria e non viene salvata su disco.
- **Lato client**: non è necessaria alcuna modifica alla logica di invio. La stampa della risposta completa era già presente nell'Exercise 0.

### Esercizio 2 — Multi-client TCP

**Versione sequenziale (`tcp_server_sequential.py`)**:
- Il singolo `accept()` del codice originale è sostituito da un loop `for` che itera fino a `MAX_CLIENTS`. Dopo che `serve_client()` ritorna (cioè dopo la disconnessione del client), il ciclo torna automaticamente ad `accept()` in attesa del client successivo.
- `MAX_CLIENTS` fornisce una condizione di terminazione pulita al server.

**Versione threaded (`tcp_server_threaded.py`)**:
- Ogni chiamata ad `accept()` lancia un nuovo `threading.Thread` con `target=serve_client`. Il thread principale ritorna immediatamente ad `accept()` senza aspettare che il client corrente si disconnetta, consentendo connessioni simultanee.
- `daemon=True` assicura che tutti i thread figli vengano terminati automaticamente quando il processo principale riceve `KeyboardInterrupt`, evitando thread orfani.
- Non è necessario alcun lock perché ogni thread opera su un proprio oggetto socket distinto, senza condividere stato mutabile.

### Esercizio 3 — Simulazione canale inaffidabile

- **`DROP_PROBABILITY`**: costante float nell'intervallo `[0.0, 1.0]` che controlla la frequenza di perdita simulata. Il valore predefinito `0.3` equivale al 30%.
- **`should_drop()`**: chiama `random.random()` che restituisce un float uniforme in `[0, 1)`. Se il valore è inferiore a `DROP_PROBABILITY`, la risposta viene scartata tramite `continue`, saltando la chiamata a `sendto()`.
- **Lato client**: `send_ping()` ora restituisce un booleano (`True` se la risposta è arrivata, `False` in caso di timeout). Il valore di ritorno viene usato in `main()` per aggiornare un contatore `received`, così il client può stampare un riepilogo finale come `Received 7/10 replies`.

### Esercizio 4 — Calcolatrice (protocollo custom TCP)

**Scelta del protocollo — TCP**:
un calcolatore è un servizio request-response dove la correttezza del risultato è fondamentale. TCP garantisce consegna e ordinamento, eliminando la necessità di implementare manualmente acknowledgment e ritrasmissione come sarebbe necessario con UDP.

**Formato messaggi (plain text UTF-8)**:

| Direzione | Messaggio | Risposta |
|---|---|---|
| Client → Server | `3 + 4` | `RESULT: 7` |
| Client → Server | `10 / 0` | `ERROR: Division by zero` |
| Client → Server | `espressione errata` | `ERROR: <descrizione>` |
| Client → Server | `QUIT` | `BYE` + chiusura connessione |

**`evaluate_expression()`**: usa `eval()` con un namespace ristretto `{"__builtins__": {}}` per impedire l'esecuzione di codice arbitrario (es. `__import__('os').system(...)`). Qualsiasi espressione non valida viene catturata da `except Exception` e restituita come messaggio di errore senza terminare il server.

**Terminazione**: il client invia `QUIT`; il server risponde `BYE`, chiude la connessione e torna in `accept()` per il client successivo.
