FROM python:3.9

# Skapa nödvändiga kataloger
RUN mkdir -p /var/www/html/flags \
    && mkdir -p /var/www/html/static \
    && mkdir -p /var/www/html/templates \
    && mkdir -p /root/flags  # ✅ Skapar katalogen innan vi skriver filen

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

# ✅ Skapa den riktiga flaggan nu när /root/flags garanterat existerar
RUN echo "O24{pharaohs_secret_tomb_uncovered}" > /root/flags/true_flag.txt

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
