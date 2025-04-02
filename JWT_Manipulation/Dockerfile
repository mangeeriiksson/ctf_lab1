FROM python:3.9-slim

# Installera beroenden
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssl \
    && rm -rf /var/lib/apt/lists/*

# Sätt arbetskatalog
WORKDIR /app

# Kopiera requirements först för cache-effektivitet
COPY requirements.txt .

# Installera Python-paket
RUN pip install --no-cache-dir -r requirements.txt

# Kopiera resterande filer
COPY . .

# Se till att flagg- och nyckelmapp finns
RUN mkdir -p flags static templates

# Rätt filrättigheter (inte nödvändigt men bra vana)
RUN chmod 600 ec_private.pem && chmod 644 ec_public.pem || true

# Exponera port för Flask
EXPOSE 6001

# Kör appen med waitress i production mode
CMD ["python", "-m", "waitress", "--port=6001", "--host=0.0.0.0", "app:app"]
