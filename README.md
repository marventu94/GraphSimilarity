# Proyecto de Detección de Similitudes en Grafos de Conocimiento

## Descripción

Este proyecto se centra en el desarrollo de un servicio web (API) que expone un modelo de red neuronal diseñado para detectar relaciones de igualdad (sameAs) en un grafo conocido. El objetivo principal es identificar entidades duplicadas dentro del grafo.

El servicio incluye una caché con una duración configurable de un día (ajustable a través de propiedades) para almacenar las respuestas, lo que permite reducir la carga sobre la red neuronal y optimizar su rendimiento.

## Tipos de Usuarios

El servicio utiliza un modelo de red neuronal previamente entrenado para evaluar la similitud de una entidad con otras 10 dentro de un grafo conocido. Cada cliente de la plataforma debe autenticarse mediante una API Key, incluida en el encabezado HTTP Authorization.

El control de solicitudes al servicio se gestiona según el tipo de cuenta del cliente, con los siguientes límites configurables a través de propiedades:

- **FREEMIUM**: 5 solicitudes por minuto.
- **PREMIUM**: 50 solicitudes por minuto.

Estos límites aseguran un acceso controlado y adaptable a las necesidades de los diferentes tipos de clientes.

## Arquitectura de Microservicios

## Descripción

La aplicación está diseñada con una arquitectura basada en microservicios, cada uno con responsabilidades específicas:

- **Autenticador**: Se encarga de la autenticación y autorización mediante API Keys, actuando además como la puerta de entrada al sistema para todas las solicitudes.
- **Logger**: Registra cada solicitud, incluyendo detalles como el tiempo de entrada, tiempo de salida y el usuario asociado.
- **Caché**: Almacena respuestas de baja volatilidad para optimizar el rendimiento y reducir la carga en los demás servicios.
- **Red Neuronal**: Procesa las solicitudes evaluando la similitud entre entidades y devuelve un resultado.

Para obtener información más detallada sobre las definiciones de diseño de los microservicios utilizados en este proyecto, consulta el archivo [ADR001-microservice-style.md](./ADRs/ADR001-microservice-style.md). Este documento describe las decisiones arquitectónicas tomadas y las razones que las respaldan.

Además, se incluyen archivos adicionales que explican en detalle el diseño de cada microservicio. Puedes revisarlos para obtener más información específica sobre su implementación:

- Autenticador: [ADR002-auth_service.md](./ADRs/ADR002-auth_service.md)
- Logger: [ADR003-logger_service.md](./ADRs/ADR003-logger_service.md)
- Caché: [ADR004-cache_service.md](./ADRs/ADR004-cache_service.md)
- Red Neuronal: [ADR005-neural_service.md](./ADRs/ADR005-neural_service.md)

Estos documentos proporcionan una visión detallada del diseño, decisiones y funcionalidades de cada componente.

### Flujo de Procesamiento de Solicitudes

En esta sección, se presenta el flujo de procesamiento de solicitudes dentro de la aplicación, ilustrado mediante un diagrama para facilitar su comprensión. El diagrama detalla cómo las llamadas avanzan a través de los diferentes microservicios, destacando los puntos clave de validación y los condicionales que determinan el camino que sigue cada solicitud

![Diagrama de Secuencia](./diagrama.jpeg "Representación de las llamadas entre microservicios")

 A continuación, se analiza cada paso del flujo, enfatizando su propósito y lógica de ejecución:

1. **Recepción de la Solicitud**  
   El servicio de autenticación recibe la solicitud y actúa como la puerta de entrada al sistema.

2. **Autenticación del Usuario**  
   - Se buscan los datos del usuario para confirmar si está registrado y determinar su tipo de cuenta (**FREEMIUM** o **PREMIUM**).
   - Se verifica que la contraseña proporcionada sea correcta.

3. **Validación de Límite de Solicitudes**  
   - Con el tipo de usuario identificado, se evalúa si realizó solicitudes en el último minuto.
   - Si se detectan solicitudes previas, se verifica si están dentro del límite permitido según su tipo de cuenta.

4. **Envío al Microservicio de Logging**  
   - La solicitud es enviada al microservicio de logging.

5. **Registro de la Solicitud de Entrada**  
   - El microservicio de logging registra la solicitud en la base de datos, incluyendo información como el usuario, la hora y los datos recibidos.

6. **Derivación al Microservicio de Caché**  
   - La solicitud es enviada al microservicio de caché.

7. **Gestión de Caché**  
   - El microservicio de caché realiza las siguientes acciones:
     - **(a)** Verifica si la solicitud ya está almacenada. Si está en la caché, devuelve la respuesta directamente, evitando el procesamiento adicional por parte de la red neuronal.
     - **(b)** Si la información no está en la caché o ha expirado, realiza una llamada al microservicio de red neuronal para recalcular la probabilidad de similitud.

8. **Devolución de la Respuesta desde la Caché**  
   - El microservicio de caché envía la respuesta obtenida al microservicio de logging, indicando si la respuesta provino de la caché o de la red neuronal.

9. **Registro de la Respuesta Final**  
   - El microservicio de logging registra la respuesta final, incluyendo el tiempo total de procesamiento.

10. **Envío al Servicio de Autenticación**  
    - La respuesta completa es enviada desde el microservicio de logging de vuelta al servicio de autenticación.

11. **Respuesta al Cliente**  
    - Finalmente, el servicio de autenticación responde al cliente con los resultados obtenidos.


## Solicitudes y Respuestas del Servicio

En esta sección, se describe el formato de las solicitudes esperadas por el servicio y la estructura de las respuestas devueltas. Se detallan las validaciones aplicadas al input y las condiciones necesarias para el procesamiento de las solicitudes. Además, se incluyen ejemplos para facilitar la comprensión

### Solicitud (Request)

El servicio acepta una solicitud en formato JSON con la siguiente estructura:

1. Input como URI: Representa una entidad dentro del grafo, especificada mediante una URI.
Ejemplo:

   ```json
   {
      "input": "https://raw.githubusercontent.com/jwackito/csv2pronto/main/ontology/pronto.owl#space_site3_50561744"
   }
   ```

2. Input como ID numérico: Representa un identificador único de una entidad en la **triplefactory**.
Ejemplo:

   ```json
   {
      "input": 106110
   }
   ```

Ambos formatos son compatibles, pero deben cumplir con las siguientes validaciones antes de ser procesados:

* **Formato válido**: El campo input debe ser una URI o un número entero.
* **Existencia de la entidad**: La entidad especificada debe existir en el grafo de entrenamiento. Dado el tipo de grafo utilizado, este es un requisito obligatorio para evitar resultados inconsistentes.

### Respuesta (Response)

El servicio devuelve una respuesta en formato JSON con la siguiente estructura:

```json
{
    "cached": false,
    "result": [
        [
            "https://raw.githubusercontent.com/jwackito/csv2pronto/main/ontology/pronto.owl#space_site2_A1552552768",
            -14.311209678649902
        ],
        [
            "https://raw.githubusercontent.com/jwackito/csv2pronto/main/ontology/pronto.owl#space_site2_A1377663274",
            -14.149275779724121
        ],
        ...
    ]
}
```

Descripción de los campos:

* **cached**: Indica si la respuesta proviene de la caché (true) o del microservicio de red neuronal (false).
Si es true, la respuesta fue almacenada previamente en la caché.
Si es false, el resultado fue calculado por el modelo de red neuronal en tiempo real.

* **result**: Es una lista de los 10 principales candidatos encontrados para la relación sameAs. Cada elemento contiene:

   * URI de la entidad: Identificador único de la entidad candidata.

   * Score: Valor numérico que representa la similitud calculada por el modelo.

## Registros de Aplicación (Logs)

Se guardan en la carpeta logs y el archivo llamado `service.log`

## Postman Collection

Se incluye una colección de Postman denominada `GraphSimilarity.postman_collection.json` para facilitar la realización de pruebas de forma rápida y eficiente.


## Configuración y Ejecución del Proyecto

## Requisitos Previos

- **Docker**: Necesario para ejecutar Redis en un contenedor.
- **Docker-Compose**: Utilizado para orquestar el inicio de servicios y microservicios.
- **Python 3**: Requerido para la ejecución de los microservicios.
- **Librerías de Python**: Especificadas en el archivo `requirements.txt` en cada microservicio

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

### Instrucciones para Levantar el Proyecto Utilizando Docker compose

Sigue estos pasos para levantar el proyecto utilizando Docker Compose:

1. **Construir las imágenes necesarias**  
   Ejecuta el siguiente comando para generar las imágenes necesarias para el proyecto:

   ```bash
   docker-compose build
   ```

2. **Iniciar los microservicios**
   Una vez generadas las imágenes, levanta todos los microservicios junto con sus dependencias ejecutando:
   
   ```bash
   docker-compose up -d
   ```
3. **Detener contenedores y eliminar imagenes**
   Si necesitas limpiar las imágenes creadas, ejecuta el siguiente comando:
  
  ```bash
  docker-compose down
   ```

## Consideraciones de Seguridad y Trabajo Futuro

- El servicio no incluye un endpoint para el registro de nuevos usuarios en la plataforma.
- Aspectos de seguridad adicionales, como el uso de API Keys internas o la implementación de redes privadas virtuales (VPC), no fueron considerados, ya que están fuera del alcance de este trabajo práctico.
- No se han aplicado medidas de seguridad específicas para Redis ni MongoDB en esta versión del proyecto.