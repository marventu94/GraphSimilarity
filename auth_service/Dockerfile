# Usar una imagen base oficial de Python
FROM python:3.12.3

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de requisitos
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar los archivos del servicio (esto puede variar por servicio)
COPY . .

# Establecer el comando por defecto como Python
CMD ["python3", "app.py"]
