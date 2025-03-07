FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN mkdir -p /app/templates /app/static/papyrus /app/flags  
COPY templates /app/templates  
CMD ["python", "app.py"]