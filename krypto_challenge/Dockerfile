# Använd en lättvikts-Python-bild
FROM python:3.10-slim

# Sätt arbetsmappen i containern
WORKDIR /app

# Kopiera över nödvändiga filer
COPY requirements.txt .
COPY app /app

# Installera beroenden
RUN pip install --no-cache-dir -r requirements.txt

# Exponera port 5000 för Flask-servern
EXPOSE 6005

# Starta Flask-servern
CMD ["python", "/app/server.py"]
