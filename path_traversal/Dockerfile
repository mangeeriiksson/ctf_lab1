FROM python:3.9

# Skapa en icke-root-användare
RUN useradd -m flaskuser

# Skapa nödvändiga kataloger och ge fulla rättigheter
RUN mkdir -p /var/www/html/flags /var/www/html/static /var/www/html/templates /root/flags \
    && chown -R flaskuser:flaskuser /var/www/html \
    && chmod -R 777 /var/www/html/flags \
    && echo "O24{pharaohs_secret_tomb_uncovered}" > /root/flags/true_flag.txt

# Växla till den icke-root-användaren
USER flaskuser

WORKDIR /var/www/html

# Kopiera requirements.txt FÖRST för att undvika onödiga ombyggnader
COPY requirements.txt /var/www/html/

# Installera Python-paket
RUN pip install --no-cache-dir -r /var/www/html/requirements.txt

# Kopiera resterande filer
COPY --chown=flaskuser:flaskuser app.py /var/www/html/
COPY --chown=flaskuser:flaskuser templates/ /var/www/html/templates/
COPY --chown=flaskuser:flaskuser static/ /var/www/html/static/
COPY --chown=flaskuser:flaskuser flags/ /var/www/html/flags/

# Exponera Flask-porten
EXPOSE 5000

# Starta Flask-applikationen
CMD ["python", "app.py"]
