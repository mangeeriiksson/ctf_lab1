FROM python:3.9

# Skapa en icke-root-användare
RUN useradd -m flaskuser

# Skapa nödvändiga kataloger
RUN mkdir -p /var/www/html/flags \
    && mkdir -p /var/www/html/static \
    && mkdir -p /var/www/html/templates \
    && mkdir -p /root/flags

# Ändra ägare till flaskuser
RUN chown -R flaskuser:flaskuser /var/www/html

# Växla till den icke-root-användaren
USER flaskuser

WORKDIR /var/www/html

# Kopiera requirements.txt FÖRST för att undvika onödiga ombyggnader
COPY requirements.txt /var/www/html/

# Installera Python-paket
RUN pip install --no-cache-dir -r /var/www/html/requirements.txt

# Kopiera resterande filer
COPY app.py /var/www/html/
COPY templates/ /var/www/html/templates/
COPY static/ /var/www/html/static/
COPY flags/ /var/www/html/flags/

# Skapa den riktiga flaggan
RUN echo "O24{pharaohs_secret_tomb_uncovered}" > /root/flags/true_flag.txt

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
