FROM python:3.9-slim

# Installera systemberoenden och ta bort cache för att hålla bilden liten
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    openssl \
    && rm -rf /var/lib/apt/lists/*

# Uppgradera pip till senaste versionen
RUN pip install --upgrade pip

# Sätt arbetskatalog
WORKDIR /app

# Kopiera requirements.txt först för cache-effektivitet
COPY requirements.txt .

# Installera Python-paket från requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Kopiera övriga filer till containern
COPY app.py .
COPY templates/ templates/
COPY static/ static/

# Kopiera EC-nyckelfilerna till containern
COPY ec_private.pem .
COPY ec_public.pem .

# Se till att flagg- och nyckelmapp finns
RUN mkdir -p flags static templates

# Rätt filrättigheter (bra vana men inte nödvändigt)
RUN chmod 600 ec_private.pem && chmod 644 ec_public.pem || true

# Exponera porten som Flask kommer att använda
EXPOSE 6001

# Starta appen med waitress i production mode
CMD ["python", "-m", "waitress", "--port=6001", "--host=0.0.0.0", "app:app"]
