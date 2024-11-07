# Proyecto de Detección de Similitudes en Grafos de Conocimiento

Este proyecto consiste en el desarrollo de un servicio web (API) que expone un modelo de red neuronal para detectar similaridades en grafos de conocimiento. El objetivo es identificar si subgrafos hablan de la misma entidad, facilitando la eliminación de duplicados en grafos de conocimiento.

## Descripción del Proyecto

El servicio utiliza un modelo de red neuronal previamente entrenado que evalúa la similitud entre dos conjuntos de propiedades de subgrafos. Cada cliente de la plataforma debe autenticarse mediante una API Key, la cual se incluye en el encabezado HTTP `Authorization`. Las solicitudes al servicio son controladas de acuerdo con el tipo de cuenta del cliente, permitiendo hasta un máximo de solicitudes por minuto:

- **FREEMIUM**: 5 solicitudes por minuto.
- **PREMIUM**: 50 solicitudes por minuto.


### Requerimientos del Proyecto

El servicio debe cumplir con los siguientes requerimientos:

1. **Autenticación y Autorización**: Cada solicitud debe incluir una API Key en el encabezado `Authorization`. Las solicitudes sin una API Key válida deben ser rechazadas.
2. **Limitación de Solicitudes**: Según el tipo de suscripción del cliente, se limita la cantidad de solicitudes permitidas por minuto.
3. **Registro de Logs**: Cada solicitud debe ser registrada, incluyendo el tiempo total de procesamiento.
4. **Caché**: Se implementa un sistema de cache para datos de solo lectura y de baja volatilidad, con el fin de mejorar el rendimiento.
5. **Modelo de Redes Neuronales**: El microservicio de red neuronal debe procesar la similitud y devolver un resultado con la probabilidad de similitud entre los subgrafos.

### Respuesta del Servicio

Para una solicitud que evalúa la similitud de subgrafos, el resultado esperado es un JSON con la probabilidad de similitud. Ejemplo de respuesta:

```json
{
    "probabilidad": 0.7
}
```
### Aclaraciones técnicas

El sistema está compuesto por varios microservicios, donde el **Microservicio de Autenticación** actúa como la puerta de entrada al servicio. Este microservicio es responsable de la autenticación y autorización de los usuarios mediante una API Key. Los demás microservicios (logger, caché y modelo de redes neuronales) no cuentan con protección adicional de acceso, por lo que existen dos opciones de despliegue recomendadas para garantizar la seguridad:

1. **Uso de API Keys Internas**: Asignar una API Key para cada comunicación entre microservicios.
2. **Despliegue en una VPC (Virtual Private Cloud)**: Embeber todos los microservicios dentro de una VPC y configurar un túnel de red para que únicamente 
el microservicio de autenticación tenga salida a internet. Esto asegura que solo los usuarios autenticados puedan acceder al sistema.

### Registros de Aplicación (Logs)

Se guardan en la carpeta logs y el archivo se llama service.log


## Configuración y Ejecución del Proyecto

Requisitos Previos

- Docker: para ejecutar Redis en un contenedor.
- Python 3: para ejecutar los microservicios.
- Librerías de Python: especificadas en requirements.txt

### Estructura del Proyecto

```
project-root/
├── auth_service/
├── cache_service/
├── logger_service/
├── neural_service/
└── requirements.txt
```

### Usuarios Registrados

La plataforma no cuenta con un sistema de registro de usuarios. Sin embargo, existen usuarios predefinidos con credenciales y tipos de suscripción para pruebas:

- freemium_user: Usuario con cuenta FREEMIUM, contraseña password123.
- premium_user: Usuario con cuenta PREMIUM, contraseña password456.

Estos usuarios se pueden utilizar para obtener una API Key y realizar pruebas de acceso según el tipo de cuenta.

### Instrucciones para Levantar el Proyecto

#### 1. Levantar Redis usando Docker

Este proyecto utiliza Redis como sistema de caché. Para iniciar Redis, ejecuta:

```
docker run -d -p 6379:6379 --name redis redis:latest
```

Para detenerlo:

```
docker stop redis
```

#### 2. Instalar Dependencias

En la raíz del proyecto, instala las dependencias de Python listadas en requirements.txt:

```
pip install -r requirements.txt
```

#### 3. Iniciar los Microservicios

Cada microservicio se ejecuta independientemente para manejar distintas funciones:

- Servicio de Autenticación: Gestiona la autenticación y autorización mediante API Keys.
- Servicio de Caché: Verifica y almacena respuestas de baja volatilidad.
- Servicio de Logger: Registra cada solicitud, incluyendo el tiempo de entrada, salida y usuario.
- Servicio de Redes Neuronales: Simula la evaluación de similitud entre subgrafos.

Para iniciar cada microservicio, ejecuta los siguientes comandos en la raíz del proyecto:

```
python3 auth_service/app.py

python3 cache_service/app.py

python3 logger_service/app.py

python3 neural_service/app.py
```
