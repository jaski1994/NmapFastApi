# NmapFastApi 

Un'API REST asincrona e veloce per eseguire scansioni Nmap. Sviluppata con **FastAPI**, **SQLAlchemy** (SQLite) e **python-nmap**. 
Gestisce le scansioni in background utilizzando `BackgroundTasks` e salva la cronologia e i risultati in un database locale.

## Funzionalità 
- **Scansioni Asincrone:** Avvia scansioni Nmap che vengono eseguite in background senza bloccare l'API.
- **Endpoint RESTful:** Crea scansioni, controlla il loro stato e recupera i risultati dettagliati (porte, stati, servizi) in formato JSON.
- **Dockerizzato:** Pronto all'uso per essere deployato con Docker e Docker Compose.
- **Diversi Tipi di Scansione:** Supporto nativo per scansioni rapide (Quick), complete (Full) e rilevamento dei servizi (Service Detection).
- **CI/CD:** Pipeline GitHub Actions preconfigurata per buildare e caricare l'immagine Docker sul GitHub Container Registry (GHCR).

## Stack Tecnologico 
- **Framework:** FastAPI, Uvicorn
- **Database:** SQLAlchemy, SQLite
- **Libreria di Rete:** Nmap, python-nmap
- **Deploy:** Docker, Docker Compose

---

## Avvio Rapido (Docker) 

Il modo più semplice e consigliato per avviare l'API è utilizzare Docker Compose, in quanto installerà automaticamente le dipendenze di sistema richieste da `nmap`.

1. **Clona la repository:**
   ```bash
   git clone https://github.com/jaski1994/NmapFastApi.git
   cd NmapFastApi
   ```

2. **Avvia i container:**
   ```bash
   docker compose up -d --build
   ```

3. **Controlla la Documentazione dell'API (Swagger & ReDoc):**
   FastAPI genera **automaticamente** la documentazione interattiva. Una volta avviato il server, apri il browser a questi indirizzi:
   - **Swagger UI** (per testare interattivamente): [http://localhost:8000/docs](http://localhost:8000/docs)
   - **ReDoc** (per documentazione più dettagliata): [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Endpoint dell'API 

L'API è esposta sotto il prefisso `/api/v1/scan/`.

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| **POST** | `/api/v1/scan/` | Avvia una nuova scansione. Richiede il `target` (es. `127.0.0.1`) e lo `scan_type` nel body della richiesta. |
| **GET** | `/api/v1/scan/` | Elenca tutte le scansioni (ordinate dalla più recente). |
| **GET** | `/api/v1/scan/{scan_id}` | Controlla lo stato di una scansione specifica (`pending`, `running`, `completed`, `failed`). |
| **GET** | `/api/v1/scan/{scan_id}/results`| Recupera i risultati completi e parsati (porte e stato) di una scansione completata. |

### Tipi di Scansione Validi (Scan Types)
- `quick`: Scansione veloce (`-T4 -F`)
- `full`: Scansiona tutte le 65535 porte (`-T4 -p-`)
- `service_detection`: Rileva le versioni dei servizi in esecuzione (`-sV`)

### Esempi di Utilizzo (cURL)

**1. Avvia una scansione:**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/scan/' \
  -H 'Content-Type: application/json' \
  -d '{
  "target": "127.0.0.1",
  "scan_type": "quick"
}'
```

**2. Elenca tutte le scansioni create:**
```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/scan/' \
  -H 'accept: application/json'
```

**3. Ottieni lo stato di una singola scansione:**
```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/scan/<id-restituito-dalla-post>' \
  -H 'accept: application/json'
```

**4. Recupera i risultati completi (se completata):**
```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/scan/<id-restituito-dalla-post>/results' \
  -H 'accept: application/json'
```

---

## CI/CD Pipeline 

Il progetto include un workflow **GitHub Actions** (`.github/workflows/ci.yml`).
Ogni volta che fai un push (o pull request) sul branch `main`:
1. Verrà eseguito il checkout del codice.
2. Viene effettuato il login al **GitHub Container Registry (GHCR)** con i permessi necessari.
3. L'immagine Docker (`nmap-api`) viene costruita e taggata.
4. L'immagine viene poi **pusherata automaticamente** sul tuo registry all'indirizzo `ghcr.io/jaski1994/nmapfastapi`.

---

## Sviluppo Locale 💻

Se desideri eseguire il progetto localmente senza Docker:

1. **Installa Nmap sul tuo sistema** (richiesto da `python-nmap`):
   ```bash
   sudo apt-get install -y nmap  # Debian/Ubuntu
   # o `brew install nmap` su macOS
   ```

2. **Configura l'Ambiente Virtuale (Virtual Environment):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Avvia il server FastAPI:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
