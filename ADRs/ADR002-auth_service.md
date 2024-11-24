
# ADR002: Diseño del Servicio de Autenticación

## Contexto

En el proyecto **GraphSimilarity**, es fundamental garantizar que solo usuarios autenticados y autorizados accedan a los servicios disponibles. Para ello, se implementa un servicio de autenticación que valida las credenciales de los usuarios y gestiona sus permisos.

## Decisión

Se ha decidido desarrollar un microservicio dedicado a la autenticación y autorización de usuarios, denominado **Auth Service**. Este servicio se encargará de:

- **Validar credenciales**: Verificar que las credenciales proporcionadas por el usuario sean correctas.
- **Generar tokens de acceso**: Emitir tokens que permitan a los usuarios autenticados acceder a otros servicios.
- **Gestionar permisos**: Determinar los niveles de acceso según el tipo de cuenta del usuario (por ejemplo, FREEMIUM o PREMIUM).
- **Controlar el límite de solicitudes (Rate Limit)**: Restringir la cantidad de solicitudes permitidas por usuario dentro de un intervalo de tiempo definido.

## Detalles de Implementación

- **API Key**: Cada cliente debe autenticarse mediante una API Key, incluida en el encabezado HTTP `Authorization`.
- **Límites de solicitudes**: Según el tipo de suscripción del cliente, se establecen límites de solicitudes por minuto:
  - **FREEMIUM**: Hasta 5 solicitudes por minuto.
  - **PREMIUM**: Hasta 50 solicitudes por minuto.
  Estos límites son configurables a través de propiedades.
- **Gestión de Rate Limit con Memoria**: El control del límite de solicitudes por usuario se implementa utilizando la memoria RAM del servidor. Para cada usuario, se guarda un contador de solicitudes y una marca de tiempo para verificar si está dentro del límite establecido. Este enfoque en memoria permite una alta velocidad de validación y elimina la necesidad de acceder a bases de datos externas para esta tarea.
- **Registro de actividad**: Cada solicitud se registra, incluyendo el tiempo total de procesamiento, para monitoreo y auditoría.
- **Caché**: Se implementa un sistema de caché con una duración configurable (por defecto, un día) para almacenar respuestas y reducir la carga sobre la red neuronal.

## Justificación

La implementación de un servicio de autenticación dedicado permite:

- **Seguridad**: Garantizar que solo usuarios autorizados accedan a los servicios.
- **Escalabilidad**: Facilitar la gestión de usuarios y permisos de manera modular.
- **Mantenimiento**: Centralizar la lógica de autenticación y autorización, simplificando futuras actualizaciones o mejoras.
- **Eficiencia del Rate Limit en Memoria**: Utilizar la memoria para la gestión del límite de solicitudes ofrece un rendimiento óptimo al eliminar latencias relacionadas con el acceso a bases de datos externas. Este enfoque es ideal para sistemas de baja complejidad o entornos controlados donde los recursos del servidor son confiables.

## Consideraciones Futuras

- **Expiración y renovación de tokens**: Implementar mecanismos para la expiración de tokens y servicios para su renovación.
- **Mejoras de seguridad**: Incorporar medidas adicionales, como el uso de API Keys internas y redes privadas virtuales (VPC).
- **Registro de usuarios**: Desarrollar endpoints que permitan el registro de nuevos usuarios en la plataforma.
- **Persistencia del Rate Limit**: Evaluar la posibilidad de persistir los datos del límite de solicitudes en una base de datos externa para mejorar la resiliencia en caso de reinicio del servidor.

Este documento detalla las decisiones arquitectónicas relacionadas con el servicio de autenticación y servirá como referencia para futuras implementaciones y mejoras.
