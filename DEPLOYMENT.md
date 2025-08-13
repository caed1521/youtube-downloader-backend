# 🚀 Guía de Despliegue - YouTube Downloader

## Arquitectura de Despliegue
- **Frontend**: Netlify (archivos estáticos)
- **Backend**: Railway (Python + FFmpeg)

## 📋 Pasos para el Despliegue

### 1. Preparar el Backend en Railway

1. **Crear cuenta en Railway**:
   - Ve a [railway.app](https://railway.app)
   - Registrate con GitHub

2. **Subir el código**:
   ```bash
   cd backend/
   git init
   git add .
   git commit -m "Initial backend setup"
   git remote add origin https://github.com/tu-usuario/youtube-downloader-backend.git
   git push -u origin main
   ```

3. **Crear proyecto en Railway**:
   - New Project → Deploy from GitHub repo
   - Selecciona tu repositorio del backend
   - Railway detectará automáticamente Python

4. **Configurar variables de entorno**:
   - En Railway Dashboard → Variables
   - Agregar: `ALLOWED_ORIGINS=https://tu-app.netlify.app`
   - Railway configurará automáticamente `PORT` y `PYTHONPATH`

5. **Obtener URL del backend**:
   - Railway te dará una URL como: `https://tu-app.railway.app`

### 2. Preparar el Frontend en Netlify

1. **Actualizar configuración**:
   - Edita `config.js`
   - Cambia `API_BASE_URL` en production por tu URL de Railway

2. **Subir a GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial frontend setup"
   git remote add origin https://github.com/tu-usuario/youtube-downloader-frontend.git
   git push -u origin main
   ```

3. **Desplegar en Netlify**:
   - Ve a [netlify.com](https://netlify.com)
   - New site from Git → GitHub
   - Selecciona tu repositorio del frontend
   - Build settings: dejar en blanco (archivos estáticos)
   - Deploy!

### 3. Configuración Final

1. **Actualizar CORS en Railway**:
   - En Railway → Variables
   - `ALLOWED_ORIGINS=https://tu-app.netlify.app`

2. **Actualizar URL del API**:
   - Edita `config.js` con tu URL real de Railway
   - Commit y push para que Netlify se actualice automáticamente

## 🔧 Archivos de Configuración Creados

- `backend/Procfile` - Comando de inicio para Railway
- `backend/railway.json` - Configuración de Railway
- `backend/nixpacks.toml` - Dependencias del sistema (Python + FFmpeg)
- `backend/.env.example` - Variables de entorno de ejemplo
- `netlify.toml` - Configuración de Netlify
- `config.js` - Configuración dinámica del API

## ✅ Verificación

1. **Backend funcionando**: Visita `https://tu-app.railway.app/health`
2. **Frontend funcionando**: Visita tu sitio de Netlify
3. **Integración**: Prueba descargar un video MP3/MP4

## 🐛 Troubleshooting

- **CORS Error**: Verifica que `ALLOWED_ORIGINS` incluya tu dominio de Netlify
- **API Error**: Verifica que la URL en `config.js` sea correcta
- **FFmpeg Error**: Railway debería instalar FFmpeg automáticamente via nixpacks.toml

## 💰 Costos Estimados

- **Railway**: Gratis hasta $5/mes de uso
- **Netlify**: Gratis para sitios estáticos
- **Total**: $0-5/mes dependiendo del tráfico
