# 🏺 Använder en officiell Python-bild
FROM python:3.9

# 🏗 Skapa arbetsmapp i containern
WORKDIR /app

# 📂 Kopiera nödvändiga filer
COPY requirements.txt requirements.txt
COPY app/ app/

# 🛠 Installera beroenden
RUN pip install --no-cache-dir -r requirements.txt

# 🚀 Starta applikationen
CMD ["python", "app/server.py"]
