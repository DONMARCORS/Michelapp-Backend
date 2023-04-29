# Michelapp-Backend

## Instalación

### Virtualenv

```bash
$ python3 -m venv .venv
```

### Activar el entorno virtual
```bash
$ source .venv/bin/activate
```

La terminal debería verse así:
```bash
(.venv) $
``` 

### Instalar dependencias
```bash
(.venv) $ pip install -r requirements.txt
```

### Crear archivo .env
```bash
(.venv) $ cp .env.example .env
```

Modificar las variables de entorno en el archivo .env


### Crear base de datos
```bash
(.venv) $ sh prestart.sh
```

### Ejecutar servidor
```bash
(.venv) $ sh run.sh
```

Una vez ejecutado el servidor, se puede acceder a la documentación en los siguientes links:

## Documentación

### Swagger
http://localhost:8001/docs

### Redoc
http://localhost:8001/redoc

### OpenAPI
http://localhost:8001/openapi.json




