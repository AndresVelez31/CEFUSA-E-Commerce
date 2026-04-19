# ── Stage: Production-ready Flask microservice ──────────────────────────────
# Base: Python slim para imagen liviana (no incluye compiladores innecesarios)
FROM python:3.12-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar dependencias primero (aprovecha cache de Docker si no cambian)
COPY requirements.txt .

# Instalar dependencias sin cache para reducir tamaño de imagen
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código fuente
COPY . .

# Puerto expuesto (debe coincidir con docker-compose.yml y nginx upstream)
EXPOSE 5000

# Health check integrado en Docker (Nginx y compose pueden detectar fallos)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Comando de arranque
CMD ["python", "app.py"]
