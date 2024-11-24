
# ADR004: Diseño del Servicio de Caché

## Contexto

En el proyecto **GraphSimilarity**, se procesan solicitudes que requieren cálculos intensivos, como la evaluación de similitud en grafos mediante un modelo de red neuronal. Para optimizar el rendimiento y reducir la carga en el microservicio de procesamiento, es necesario implementar un sistema de caché que almacene respuestas previamente calculadas.

## Decisión

Se ha decidido implementar un microservicio denominado **Cache Service**, encargado de gestionar una capa de caché que almacene las respuestas de los cálculos realizados por la red neuronal. Este servicio utilizará **Redis** como solución de almacenamiento en memoria para manejar la caché.

## Detalles de Implementación

- **Duración de la caché**:  
  Las respuestas se almacenarán en la caché con un tiempo de vida configurado (por defecto, 1 día). Este valor es configurable a través de propiedades del sistema.
  
- **Claves y valores de la caché**:  
  - **Clave**: Generada a partir de un hash único basado en el input de la solicitud.
  - **Valor**: Almacena la respuesta completa del servicio, incluyendo los resultados y metadatos relevantes.

- **Integración con Redis**:  
  - **Tecnología**: Redis ha sido seleccionada como solución de almacenamiento en memoria.
  - **Modo de operación**: Redis opera en modo "key-value", ofreciendo acceso rápido y eficiente a los datos.
  - **Conexión y configuración**: El servicio se conectará a una instancia de Redis configurada localmente o en un entorno remoto, según las necesidades de despliegue.

## Justificación

La elección de Redis como tecnología para la implementación de la caché se basa en las siguientes razones:

- **Baja latencia y alto rendimiento**: Redis es una solución de almacenamiento en memoria extremadamente rápida, lo que la hace ideal para manejar operaciones de lectura/escritura en sistemas de alto rendimiento como este.
- **Persistencia opcional**: Redis permite persistir los datos en disco, aunque no se requiere para este proyecto. Esto ofrece flexibilidad en caso de que se necesite una solución híbrida en el futuro.
- **Facilidad de uso**: Redis es fácil de configurar e integrar con servicios en múltiples lenguajes y entornos.
- **Características avanzadas**: Redis admite configuraciones adicionales como TTL (Time-to-Live) para gestionar la expiración de datos y estructuras avanzadas para manejar información compleja.
- **Ampliamente adoptada y soportada**: Redis cuenta con una amplia comunidad y documentación, asegurando soporte continuo y actualizaciones.

## Consideraciones Futuras

- **Clúster Redis**: Si el volumen de datos almacenados o la concurrencia aumenta significativamente, se puede configurar Redis en modo clúster para distribuir la carga y mejorar la escalabilidad.
- **Monitoreo de caché**: Incorporar herramientas como RedisInsight para monitorear y optimizar el uso de la caché.
- **Fallback en caso de falla**: Implementar mecanismos que permitan manejar adecuadamente las solicitudes en caso de que Redis no esté disponible, garantizando la continuidad del servicio.
- **Seguridad de Redis**: Evaluar medidas de seguridad adicionales, como la configuración de contraseñas y restricciones de acceso, para proteger la instancia de Redis en entornos de producción.

Este documento detalla las decisiones arquitectónicas relacionadas con el servicio de caché y la elección de Redis como tecnología base. Servirá como referencia para futuras implementaciones y mejoras.
