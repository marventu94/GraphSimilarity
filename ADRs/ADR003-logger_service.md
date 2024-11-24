
# ADR003: Diseño del Servicio de Logging

## Contexto

En el proyecto **GraphSimilarity**, es fundamental realizar un seguimiento de las solicitudes que ingresan y de las respuestas generadas por los microservicios. Esto permite monitorear el uso del sistema, detectar errores y realizar auditorías. Para ello, se implementa un microservicio de logging encargado de registrar toda la actividad relevante.

## Decisión

Se ha decidido implementar un microservicio dedicado, denominado **Logger Service**, que gestionará el registro de eventos clave en el sistema. Este servicio se encargará de:

- **Registrar solicitudes**: Almacenar detalles de cada solicitud recibida, como el usuario, el timestamp y el contenido de la solicitud.
- **Registrar respuestas**: Documentar las respuestas generadas, indicando si provinieron de la caché o de la red neuronal, así como el tiempo total de procesamiento.
- **Almacenar registros en un archivo `.log`**: Utilizar un archivo de texto para guardar los logs en lugar de bases de datos u otros sistemas de almacenamiento más complejos.

## Detalles de Implementación

- **Formato del archivo de logs**:  
  Los registros se guardarán en un archivo `.log` con un formato estructurado, legible y consistente. Cada entrada incluirá información clave como:
  - Timestamp
  - Usuario o cliente identificado
  - Detalles de la solicitud (endpoint, parámetros, etc.)
  - Respuesta generada (incluyendo el tiempo de procesamiento y si se utilizó la caché)
- **Rotación de archivos**: Para evitar que los archivos de log crezcan indefinidamente, se implementará un sistema de rotación. Esto implica dividir los logs en varios archivos basados en su tamaño o fecha.
- **Mecanismo de escritura asíncrona**: Los registros serán escritos de forma asíncrona para no bloquear el procesamiento de solicitudes.

## Justificación

La decisión de utilizar un archivo `.log` para guardar los registros se basa en los siguientes factores:

- **Simplicidad**: Un archivo de logs es fácil de implementar, configurar y mantener. No requiere infraestructura adicional como bases de datos o servicios externos.
- **Portabilidad**: Los archivos `.log` pueden ser transferidos y analizados fácilmente en cualquier entorno sin depender de software específico.
- **Rendimiento**: Escribir en un archivo local es rápido y eficiente, especialmente cuando se implementa un mecanismo de escritura asíncrona.
- **Escalabilidad inicial**: Para el alcance del proyecto actual, un archivo de logs es suficiente para manejar el volumen esperado de registros. En el futuro, si el sistema requiere mayor escalabilidad, se podrá migrar a una solución más robusta como Elasticsearch o un servicio de logging centralizado.

## Consideraciones Futuras

- **Integración con sistemas avanzados de logging**: En caso de necesitar un análisis más profundo o en tiempo real, los logs podrían integrarse con herramientas como ELK Stack (Elasticsearch, Logstash, Kibana) o servicios en la nube como AWS CloudWatch o Google Cloud Logging.
- **Persistencia centralizada**: Evaluar la opción de almacenar los logs en una base de datos o sistema distribuido para facilitar su consulta en entornos con múltiples instancias del servicio.
- **Cifrado de logs sensibles**: Implementar medidas de seguridad para proteger información sensible en los registros.

Este documento detalla las decisiones arquitectónicas relacionadas con el servicio de logging y servirá como referencia para futuras implementaciones y mejoras.
