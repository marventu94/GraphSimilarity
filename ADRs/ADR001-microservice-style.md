# Architecture Decision Record (ADR)

## Contexto

Este proyecto implementa un servicio web para evaluar la similitud entre subgrafos utilizando un modelo de red neuronal. El sistema está compuesto por varios microservicios:

- **Autenticador**: Gestiona la autenticación y autorización mediante API Keys.
- **Logger**: Registra las solicitudes, incluyendo tiempos de entrada, salida y usuario.
- **Caché**: Almacena respuestas de baja volatilidad para mejorar el rendimiento.
- **Red Neuronal**: Evalúa la similitud y devuelve un resultado probabilístico.

La comunicación entre estos microservicios es secuencial, con dependencias claras en el flujo de datos:

1. Autenticación y autorización.
2. Registro de logs al inicio de la solicitud.
3. Validación de caché para consultas repetidas.
4. Evaluación del modelo de red neuronal si la consulta no está en caché.
5. Registro de logs al final de la solicitud.

Este flujo secuencial garantiza la funcionalidad esperada, pero introduce un alto nivel de acoplamiento entre los microservicios.

## Decisión

Se seleccionó una **estrategia de cadena larga** debido a la naturaleza secuencial del flujo de las solicitudes. Esta decisión asegura un control lógico claro y permite la trazabilidad completa de cada solicitud a través del sistema.

- **Ventajas**:
  - Facilita la trazabilidad completa de las solicitudes.
  - Refleja de manera natural el flujo de datos esperado.
  - Simplifica la integración de nuevos microservicios en el futuro, siguiendo el patrón secuencial.

- **Limitaciones**:
  - Introduce un alto nivel de acoplamiento entre los servicios.
  - Potencial impacto en el rendimiento si uno de los servicios tiene un cuello de botella.
  - La resiliencia depende de la robustez de cada microservicio en la cadena.

## Alternativas Consideradas

1. **Orquestación Centralizada**:
   - Uso de un gestor central (e.g., Apache Kafka) para coordinar las solicitudes.
   - Rechazada por complejidad innecesaria para el alcance del proyecto actual.

2. **Estrategía de llamada ancha**:
   - El micro servicio de autenticación llama en paralelo a logger y a la cache.
   - Rechazada debido a la necesidad de volver a llamar al logger para registrar la respuesta de la caché.
