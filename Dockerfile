# ---- Base ----
FROM python:3.12-slim

# Ajustes de Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DB_DIR=/data

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias (aprovecha caché)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar código
COPY . .

# Crear carpeta de datos (para la DB)
RUN mkdir -p ${DB_DIR}

# Exponer puerto
EXPOSE 8000

# Comando de arranque (uvicorn en producción básica)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
