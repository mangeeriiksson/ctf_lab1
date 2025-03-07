# Använd Python 3.9
FROM python:3.9

# Skapa arbetsmapp
WORKDIR /app

# Kopiera alla filer till containern
COPY . /app

# Kopiera templates separat för att undvika problem
COPY templates /app/templates

# Installera Python-paket
RUN pip install --no-cache-dir -r requirements.txt

# Skapa flags-mappen och flaggfilerna
RUN mkdir -p /app/flags && echo "O24{command_of_the_pharaoh}" > /app/flags/sacred_command.txt

# Exponera Flask-porten
EXPOSE 5000

# Starta Flask-applikationen
CMD ["python", "app.py"]
