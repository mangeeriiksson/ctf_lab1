
FROM python:3.9
WORKDIR /var/www/html
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /var/www/html/templates /var/www/html/static/papyrus /var/www/html/flags /root/flags
COPY . /var/www/html
RUN echo "O24{you_have_been_tricked_by_the_pharaoh}" > /var/www/html/flags/fake_scroll_1.txt
RUN echo "O24{this_is_not_the_flag_you_seek}" > /var/www/html/flags/fake_scroll_2.txt
RUN echo "O24{the_true_treasure_is_buried_deep}" > /root/flags/ancient_scroll.txt
RUN chmod -R 755 /var/www/html /root/flags
CMD ["python", "app.py"]
