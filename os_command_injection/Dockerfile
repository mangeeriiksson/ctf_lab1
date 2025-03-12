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

# Skapa flags-mappen och flaggfilerna
RUN mkdir -p /app/flags && echo "O24{command_of_the_pharaoh}" > /app/flags/sacred_command.txt

# Ändra ägare till flaskuser
RUN chown -R flaskuser:flaskuser /app

# Byt till icke-root-användaren
USER flaskuser

# Exponera Flask-porten
EXPOSE 5001

# Starta Flask med Gunicorn för bättre prestanda
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]
