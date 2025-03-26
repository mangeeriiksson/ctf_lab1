# Använd Python 3.9 som basbild
FROM python:3.9

# Skapa en icke-root-användare
RUN useradd -m flaskuser

# Sätt arbetskatalog
WORKDIR /app

# Kopiera bara requirements.txt först för att optimera byggtiden
COPY requirements.txt /app/

# Installera Python-paket
RUN pip install --no-cache-dir -r requirements.txt

# Kopiera resterande filer
COPY . /app
COPY templates /app/templates

# 🛑 Skapa flaggorna på rätt plats:
RUN mkdir -p /root/ /app/flags/ \
    && echo "O24{command_of_the_pharaoh}" > /root/true_flag.txt \
    && echo "O24{almost_there_but_not}" > /app/flags/ancient_curse.txt

# Ändra ägare till flaskuser (för /app/)
RUN chown -R flaskuser:flaskuser /app

# Byt till icke-root-användaren
USER flaskuser

# Exponera Flask-porten
EXPOSE 6002

# Starta Flask med Gunicorn för bättre prestanda
CMD ["gunicorn", "--bind", "0.0.0.0:6002", "app:app"]
