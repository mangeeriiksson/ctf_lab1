# Använd en officiell Python-basavbildning från Docker Hub
FROM python:3.9-slim

# Sätt arbetskatalogen i containern
WORKDIR /app

# Kopiera requirements.txt och installera nödvändiga paket
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Kopiera applikationskoden till containern
COPY . .

# Exponera porten som applikationen kommer att lyssna på
EXPOSE 5000

# Kommando för att starta Flask-servern
CMD ["python", "guardian_server.py"]
