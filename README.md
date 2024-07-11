# Tomato

## Overview

Questo progetto fornisce una raccolta di API progettate per gestire entità come ristoranti, ricette e ingredienti utilizzando un framework basato su Django. Le API abilitano le seguenti funzionalità:

- **Ristoranti**: crea, aggiorna, elimina, elenca tutti i ristoranti e recupera i ristoranti associati alle ricette.

- **Ricette**: crea, aggiorna, elimina, elenca tutte le ricette e recupera ricette associate a un ristorante o ingrediente.

- **Ingredienti**: crea, aggiorna, elimina, elenca tutti gli ingredienti e recupera gli ingredienti associati a una ricetta o a un ristorante.

## Installation

Run i comandi seguenti per installare ed eseguire il progetto

```bash
# Clona il repository
git clone https://github.com/AmrAlashram/Tomato.git

# Passare alla directory del progetto
cd tomato/

# Installa le dipendenze
pip install -r requirements.txt

# Avviare il server
python manage.py runserver
```

## Docker
Inoltre, questo progetto è stato inserito in un contenitore e l'immagine Docker è disponibile sul collegamento
[Docker Image's Link](https://hub.docker.com/r/amrscode/tomato)

Per scaricare ed eseguire l'immagine docker, esegui i comandi seguenti e nota che resterà in ascolto sulla porta 8000
```bash
# Pull l'immagine docker
docker pull amrscode/tomato:latest

# Run it
docker run -p 8000:8000 amrscode/tomato:latest
```

## API Documentation
Inoltre, le API create in questo progetto sono state documentate utilizzando Postman. Per accedere alla documentazione utilizzare il seguente link
[Postman API Documentation](https://tomatoamr.postman.co/workspace/tomato_amr-Workspace~22c4768c-3e3e-442c-ba6b-a5afcf55f8cc/collection/36847207-71f505d1-3195-4611-bfd3-09339a331a28?action=share&creator=36847207)

## Database

**In Github,** Ho mantenuto il database nel repository Github a causa delle sue dimensioni ridotte, quindi non ho riscontrato la necessità di archiviarlo su una piattaforma esterna.

**In Docker** Ho mantenuto il database all'interno dell'immagine docker. In uno scenario reale, non dovrebbe trovarsi nell'immagine Docker. Per mantenere la persistenza dei dati, il database dovrebbe trovarsi sul disco e i <u>volumi</u> dovrebbero essere utilizzati per consentire al contenitore docker di accedere al database. Tuttavia, nel nostro caso, si tratta semplicemente di un compito semplice che non può essere distribuita, quindi mantenerla nell'immagine docker è il modo migliore per mantenere la similitudine.