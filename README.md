# Features / Funcionalidades
## English
- Session validation using JWT, cache, and control checks to determine whether a user is banned or flagged as suspicious.
- Design guidelines that allow the platform to be scalable and easily maintainable.
- Automatic email alerts sent to all users with the "BACKEND DEVELOPER" role when something unusual happens.
- Detailed logs during execution of each service.
- Each request is stored in a ```requests``` table in the database for metrics and tracing.
This could be improved by integrating Kafka, Grafana, or Prometheus, but due to time constraints, I chose to insert the records directly.

# Español
- Validación de sesión mediante JWT, caché y verificaciones de control relacionadas con si un usuario fue baneado o marcado como sospechoso.
- Lineamientos de diseño que permiten que la plataforma sea escalable y fácilmente mantenible.
- Envío automático de alertas por correo electrónico a todos los usuarios con el rol "BACKEND DEVELOPER" cuando ocurre algo inusual.
- Registros detallados durante la ejecución de cada servicio.
- Cada petición se guarda en la tabla ```requests``` de la base de datos para métricas y trazas.
Esto podría mejorarse integrando Kafka, Grafana o Prometheus, pero por cuestiones de tiempo decidí realizar la inserción directamente.

# Usage / Uso
## English
First of all, the repository must be cloned and accessed
```bash
    git clone https://github.com/apps-grupo-6/backend.git
    cd backend
```

After that, the project can be started using any of the following options:
- Using the PowerShell helper tool:
```PowerShell
   .\run.ps1
```

- Using the Bash helper tool:
```bash
   ./run.sh
```

- Using Docker in the traditional way:
```bash
    docker compose up -d
    docker logs -f --tail 20 backend
```

# Español
Primero deberá clonarse el repositorio y acceder a su contenido
```bash
    git clone https://github.com/apps-grupo-6/backend.git
    cd backend
```

Luego, utilizando la consola, deberá iniciar el proyecto mediante alguna de las siguientes opciones:

- Utilizando nuestra herramienta mediante PowerShell:
```PowerShell
   .\run.ps1
```

- Utilizando nuestra herramienta mediante Bash:
```bash
   ./run.sh
```

- Utilizando docker de la manera tradicional:
```bash
    docker compose up -d
    docker logs -f --tail 20 backend
```

# Useful information / Información útil
## English
If for any reason the database needs to be restored, it can be done by using:

```bash
    docker compose down -v 
```
Then, the project should be started again.
If any modifications were made, it is recommended to check that the ```.initdb``` folder contains only the two initial files.

## Español
Si por algún motivo se necesita restaurar la base de datos, puede hacerse utilizando:

```bash
    docker compose down -v 
```
Y luego iniciar el proyecto nuevamente. En caso de haber modificado algo, revisar si en la carpeta ```.initdb``` solo están los 2 archivos iniciales.
