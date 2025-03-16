# Use official lightweight Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy only requirements first (for efficient caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app files
COPY . .

# Expose the Flask port
EXPOSE 5000

# Kör Flask korrekt i Docker och se till att debug fungerar
CMD ["python", "-u", "app.py"]
