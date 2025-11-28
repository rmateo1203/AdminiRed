# Guía de Despliegue en Google Cloud Platform
## AdminiRed - Configuración para Producción

### 📋 Requisitos Previos

- Cuenta en Google Cloud Platform
- Proyecto creado en GCP
- Facturación habilitada
- Conocimientos básicos de Linux y Django

---

## 🏗️ Arquitectura Recomendada

```
┌─────────────────┐
│  Load Balancer  │ (Opcional, para alta disponibilidad)
└────────┬────────┘
         │
┌────────▼────────┐
│ Compute Engine  │ (Instancia de VM)
│   (Django App)  │
└────────┬────────┘
         │
┌────────▼────────┐
│   Cloud SQL     │ (PostgreSQL)
│   (Base datos)  │
└─────────────────┘
```

---

## 🚀 Opción 1: Configuración Básica (Recomendada para empezar)

### Paso 1: Crear Instancia de Compute Engine

```bash
# Crear instancia VM
gcloud compute instances create adminired-prod \
    --zone=us-central1-a \
    --machine-type=e2-medium \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=20GB \
    --tags=http-server,https-server
```

### Paso 2: Configurar Firewall

```bash
# Permitir tráfico HTTP y HTTPS
gcloud compute firewall-rules create allow-http-https \
    --allow tcp:80,tcp:443 \
    --source-ranges 0.0.0.0/0 \
    --target-tags http-server,https-server
```

### Paso 3: Crear Base de Datos Cloud SQL

```bash
# Crear instancia de PostgreSQL
gcloud sql instances create adminired-db \
    --database-version=POSTGRES_15 \
    --tier=db-f1-micro \
    --region=us-central1 \
    --root-password=TU_PASSWORD_SEGURO
```

### Paso 4: Crear Base de Datos

```bash
# Conectarse y crear la base de datos
gcloud sql databases create adminired \
    --instance=adminired-db
```

---

## 📦 Instalación en el Servidor

### Paso 1: Conectarse al Servidor

```bash
# Obtener IP externa
gcloud compute instances describe adminired-prod \
    --zone=us-central1-a \
    --format='get(networkInterfaces[0].accessConfigs[0].natIP)'

# Conectarse por SSH
gcloud compute ssh adminired-prod --zone=us-central1-a
```

### Paso 2: Instalar Dependencias del Sistema

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python y dependencias
sudo apt install -y python3.12 python3.12-venv python3-pip \
    postgresql-client nginx supervisor git

# Instalar certificados SSL (Let's Encrypt)
sudo apt install -y certbot python3-certbot-nginx
```

### Paso 3: Configurar Usuario y Permisos

```bash
# Crear usuario para la aplicación
sudo adduser --disabled-password --gecos "" adminired
sudo usermod -aG sudo adminired

# Cambiar al usuario
su - adminired
```

### Paso 4: Clonar y Configurar la Aplicación

```bash
# Crear directorio
mkdir -p /home/adminired/app
cd /home/adminired/app

# Clonar repositorio (o subir archivos)
git clone TU_REPOSITORIO .
# O usar scp para subir archivos

# Crear entorno virtual
python3.12 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

### Paso 5: Configurar Variables de Entorno

```bash
# Crear archivo .env
nano .env
```

```env
DJANGO_ENVIRONMENT=production
SECRET_KEY=TU_SECRET_KEY_MUY_SEGURO
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,IP_DEL_SERVIDOR

# Base de datos Cloud SQL
DB_NAME=adminired
DB_USER=postgres
DB_PASSWORD=TU_PASSWORD
DB_HOST=/cloudsql/PROYECTO_ID:us-central1:adminired-db
DB_PORT=5432

# Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
```

### Paso 6: Configurar Conexión a Cloud SQL

```bash
# Instalar Cloud SQL Proxy
wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 \
    -O cloud_sql_proxy
chmod +x cloud_sql_proxy

# Mover a ubicación del sistema
sudo mv cloud_sql_proxy /usr/local/bin/

# Crear servicio systemd para Cloud SQL Proxy
sudo nano /etc/systemd/system/cloud-sql-proxy.service
```

```ini
[Unit]
Description=Cloud SQL Proxy
After=network.target

[Service]
Type=simple
User=adminired
ExecStart=/usr/local/bin/cloud_sql_proxy \
    -instances=PROYECTO_ID:us-central1:adminired-db=tcp:5432
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Habilitar y iniciar servicio
sudo systemctl enable cloud-sql-proxy
sudo systemctl start cloud-sql-proxy
```

### Paso 7: Ejecutar Migraciones

```bash
cd /home/adminired/app
source venv/bin/activate

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Recolectar archivos estáticos
python manage.py collectstatic --noinput
```

### Paso 8: Configurar Gunicorn

```bash
# Crear archivo de configuración
nano /home/adminired/app/gunicorn_config.py
```

```python
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
timeout = 120
keepalive = 5
user = "adminired"
group = "adminired"
logfile = "/home/adminired/app/logs/gunicorn.log"
loglevel = "info"
```

### Paso 9: Configurar Supervisor

```bash
# Crear directorio de logs
mkdir -p /home/adminired/app/logs

# Crear configuración de supervisor
sudo nano /etc/supervisor/conf.d/adminired.conf
```

```ini
[program:adminired]
command=/home/adminired/app/venv/bin/gunicorn \
    --config /home/adminired/app/gunicorn_config.py \
    adminired.wsgi:application
directory=/home/adminired/app
user=adminired
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/adminired/app/logs/gunicorn.log
```

```bash
# Recargar supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start adminired
```

### Paso 10: Configurar Nginx

```bash
# Crear configuración de Nginx
sudo nano /etc/nginx/sites-available/adminired
```

```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    # Redirigir a HTTPS (después de configurar SSL)
    # return 301 https://$server_name$request_uri;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/adminired/app/staticfiles/;
    }

    location /media/ {
        alias /home/adminired/app/media/;
    }
}
```

```bash
# Habilitar sitio
sudo ln -s /etc/nginx/sites-available/adminired /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Paso 11: Configurar SSL (Let's Encrypt)

```bash
# Obtener certificado SSL
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com

# Renovación automática (ya está configurada por defecto)
sudo certbot renew --dry-run
```

---

## 🔧 Configuración de Django para Producción

### Actualizar settings/production.py

```python
# Agregar configuración para Cloud SQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='127.0.0.1'),
        'PORT': config('DB_PORT', default='5432'),
        'OPTIONS': {
            'connect_timeout': 10,
        },
        'CONN_MAX_AGE': 600,
    }
}

# Configuración de seguridad
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

---

## 📊 Monitoreo y Mantenimiento

### Configurar Backups Automáticos

```bash
# Crear script de backup
nano /home/adminired/app/backup.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/adminired/backups"
mkdir -p $BACKUP_DIR

# Backup de base de datos
gcloud sql export sql adminired-db \
    gs://tu-bucket-backups/adminired_$DATE.sql \
    --database=adminired

# Backup de archivos media
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /home/adminired/app/media/

# Eliminar backups antiguos (mantener últimos 30 días)
find $BACKUP_DIR -type f -mtime +30 -delete
```

```bash
# Hacer ejecutable
chmod +x /home/adminired/app/backup.sh

# Agregar a crontab (backup diario a las 2 AM)
crontab -e
# Agregar: 0 2 * * * /home/adminired/app/backup.sh
```

### Configurar Monitoreo Básico

```bash
# Instalar herramientas de monitoreo
sudo apt install -y htop iotop

# Configurar alertas de disco
# (Configurar en Google Cloud Monitoring)
```

---

## 💰 Costos Estimados en GCP

### Configuración Básica (Pequeña)
- **Compute Engine** (e2-medium): ~$1,200 MXN/mes
- **Cloud SQL** (db-f1-micro): ~$800 MXN/mes
- **Storage** (10GB): ~$200 MXN/mes
- **Network**: ~$300 MXN/mes
- **Total**: ~$2,500 MXN/mes

### Configuración Estándar (Mediana)
- **Compute Engine** (e2-standard-2): ~$2,400 MXN/mes
- **Cloud SQL** (db-g1-small): ~$1,500 MXN/mes
- **Storage** (50GB): ~$500 MXN/mes
- **Network**: ~$600 MXN/mes
- **Total**: ~$5,000 MXN/mes

---

## 🔐 Seguridad

### Checklist de Seguridad

- [ ] SSL/HTTPS configurado
- [ ] Firewall configurado correctamente
- [ ] Secretos en variables de entorno (no en código)
- [ ] DEBUG=False en producción
- [ ] ALLOWED_HOSTS configurado
- [ ] Backups automáticos configurados
- [ ] Usuario no-root para la aplicación
- [ ] Actualizaciones de seguridad automáticas
- [ ] Logs de acceso configurados
- [ ] Monitoreo de recursos activo

---

## 📝 Scripts Útiles

### Script de Deploy Rápido

```bash
#!/bin/bash
# deploy.sh

cd /home/adminired/app
source venv/bin/activate

# Actualizar código
git pull origin main

# Instalar dependencias
pip install -r requirements.txt

# Migraciones
python manage.py migrate

# Recolectar estáticos
python manage.py collectstatic --noinput

# Reiniciar aplicación
sudo supervisorctl restart adminired

echo "Deploy completado!"
```

---

## 🆘 Troubleshooting

### Problemas Comunes

1. **Error de conexión a base de datos**
   - Verificar que Cloud SQL Proxy esté corriendo
   - Verificar credenciales en .env
   - Verificar firewall de Cloud SQL

2. **Error 502 Bad Gateway**
   - Verificar que Gunicorn esté corriendo: `sudo supervisorctl status`
   - Verificar logs: `tail -f /home/adminired/app/logs/gunicorn.log`

3. **Archivos estáticos no se muestran**
   - Ejecutar: `python manage.py collectstatic`
   - Verificar permisos de /staticfiles/
   - Verificar configuración de Nginx

---

**Última actualización**: Diciembre 2024
**Versión**: 1.0

