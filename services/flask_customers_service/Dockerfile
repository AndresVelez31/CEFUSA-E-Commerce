FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Creamos el directorio y copiamos la base de datos pre-poblada
RUN mkdir -p /data
COPY customers.db /data/customers.db

COPY . .
CMD ["python", "app.py"]
