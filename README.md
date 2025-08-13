# 🌐 YouTube MP3/MP4 Downloader

Un sitio web moderno y elegante para descargar videos de YouTube en formato MP3 (audio) o MP4 (video) con una interfaz de usuario intuitiva y diseño responsive.

## ✨ Características

- 🎵 **Descarga MP3**: Extrae audio de alta calidad (192kbps)
- 🎬 **Descarga MP4**: Videos en múltiples calidades (240p - 1080p)
- 🎨 **Diseño moderno**: Interfaz elegante con paleta de colores Netflix-style
- 📱 **Responsive**: Optimizado para móviles y tablets
- ⚡ **Rápido**: Procesamiento eficiente con yt-dlp
- 🔒 **Seguro**: Validación de URLs y manejo de errores robusto
- 📊 **Vista previa**: Información del video antes de descargar
- 🧹 **Auto-cleanup**: Limpieza automática de archivos temporales

## 🚀 Instalación y Configuración

### Requisitos previos
- Python 3.8 o superior
- Node.js (opcional, para desarrollo frontend)
- FFmpeg (para conversión de audio)

### Configuración del Backend

1. **Navegar al directorio del backend:**
   ```bash
   cd backend
   ```

2. **Crear un entorno virtual (recomendado):**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Instalar FFmpeg:**
   - **Windows**: Descargar desde [ffmpeg.org](https://ffmpeg.org/download.html)
   - **Linux**: `sudo apt install ffmpeg`
   - **Mac**: `brew install ffmpeg`

### Configuración del Frontend

1. **Servir archivos estáticos:**
   - Usar un servidor web local (Live Server, Python HTTP server, etc.)
   - O abrir directamente `index.html` en el navegador

## 🏃‍♂️ Ejecución

### Iniciar el Backend

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

El API estará disponible en: `http://localhost:8000`

### Iniciar el Frontend

**Opción 1: Servidor HTTP de Python**
```bash
# En el directorio raíz del proyecto
python -m http.server 3000
```

**Opción 2: Live Server (VS Code)**
- Instalar la extensión "Live Server"
- Click derecho en `index.html` → "Open with Live Server"

**Opción 3: Abrir directamente**
- Abrir `index.html` en el navegador
- Nota: Algunas funciones pueden requerir HTTPS/servidor local

## 📖 Uso

1. **Abrir la aplicación** en el navegador
2. **Pegar la URL** del video de YouTube
3. **Seleccionar formato**: MP3 (audio) o MP4 (video)
4. **Elegir calidad** (solo para MP4): 240p, 360p, 480p, 720p, 1080p
5. **Hacer clic en "Descargar"**
6. **Esperar el procesamiento** y hacer clic en el botón final de descarga

## 🛠️ API Endpoints

### `POST /analyze`
Analiza un video de YouTube y prepara la descarga.

**Request:**
```json
{
  "url": "https://youtube.com/watch?v=...",
  "format": "mp3|mp4",
  "quality": "720p"
}
```

**Response:**
```json
{
  "download_id": "uuid",
  "video_info": {
    "title": "Video Title",
    "thumbnail": "thumbnail_url",
    "duration": "3:45",
    "views": "1.2M visualizaciones"
  },
  "estimated_size": "25.3 MB"
}
```

### `POST /download/{download_id}`
Inicia el proceso de descarga.

### `GET /status/{download_id}`
Verifica el estado de la descarga.

### `GET /file/{download_id}`
Descarga el archivo procesado.

## 🎨 Personalización

### Colores del tema
```css
:root {
  --bg-primary: #0D0D0D;    /* Negro profundo */
  --accent: #E50914;        /* Rojo vibrante */
  --text-primary: #FFFFFF;  /* Blanco puro */
  --text-secondary: #B3B3B3; /* Gris claro */
  --bg-secondary: #1F1F1F;  /* Gris oscuro */
}
```

### Tipografías
- **Títulos**: Poppins (Google Fonts)
- **Texto general**: Inter (Google Fonts)

## 🚀 Despliegue

### Backend (Render/Railway/Heroku)

1. **Crear `Procfile`:**
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

2. **Variables de entorno:**
   - `PYTHON_VERSION=3.9`
   - Instalar FFmpeg en el contenedor

### Frontend (Netlify/Vercel)

1. **Actualizar la URL del API** en `script.js`
2. **Configurar CORS** en el backend para el dominio de producción
3. **Desplegar** los archivos estáticos

## ⚠️ Consideraciones Legales

- ✅ **Uso personal y educativo únicamente**
- ❌ **No infringir derechos de autor**
- ⚖️ **Cumplir con las leyes locales**
- 📜 **Respetar los términos de servicio de YouTube**

## 🐛 Solución de Problemas

### Error: "FFmpeg not found"
- Instalar FFmpeg y agregarlo al PATH del sistema

### Error: "CORS policy"
- Verificar que el backend esté ejecutándose
- Usar un servidor HTTP local para el frontend

### Error: "Video not available"
- El video puede tener restricciones geográficas
- Verificar que la URL sea válida y pública

### Error: "Download timeout"
- Videos muy largos pueden tardar más
- Verificar la conexión a internet

## 📝 Licencia

Este proyecto es solo para fines educativos y de demostración. Los usuarios son responsables de cumplir con las leyes de derechos de autor aplicables.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📞 Soporte

Si encuentras algún problema o tienes preguntas:

1. Revisar la sección de solución de problemas
2. Verificar que todas las dependencias estén instaladas
3. Comprobar que FFmpeg esté disponible en el PATH

---

**⚡ ¡Disfruta descargando tus videos favoritos de YouTube!**
4. Confirma la descarga
5. El video se guardará en la carpeta `downloads/`

### Versión con interfaz gráfica

Ejecuta la versión GUI:
```bash
python youtube_downloader_gui.py
```

**Pasos:**
1. Pega la URL en el campo correspondiente
2. Haz clic en "Obtener Info"
3. Selecciona la calidad de la lista
4. Opcionalmente cambia la carpeta de destino
5. Haz clic en "Descargar Video"

## 📁 Estructura de archivos

```
├── youtube_downloader.py      # Versión línea de comandos
├── youtube_downloader_gui.py  # Versión con interfaz gráfica
├── requirements.txt           # Dependencias
├── downloads/                 # Carpeta de descargas (se crea automáticamente)
└── README.md
```

## 🎯 Ejemplos de uso

### URLs compatibles:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID`

### Calidades típicamente disponibles:
- 144p (baja calidad, archivo pequeño)
- 360p (calidad estándar)
- 480p (calidad media)
- 720p (HD)
- 1080p (Full HD)
- 1440p (2K) - si está disponible
- 2160p (4K) - si está disponible

## ⚠️ Consideraciones importantes

1. **Uso legal:** Solo descarga videos que tengas derecho a descargar
2. **Derechos de autor:** Respeta los derechos de autor del contenido
3. **Términos de servicio:** Revisa los términos de servicio de YouTube
4. **Uso personal:** Este programa está diseñado para uso personal y educativo

## 🔧 Solución de problemas

### Error: "yt-dlp no está instalado"
```bash
pip install yt-dlp
```

### Error: "No se encontraron formatos MP4"
- El video puede no estar disponible en MP4
- Intenta con otro video
- Verifica que la URL sea correcta

### Error de conexión
- Verifica tu conexión a internet
- Algunos videos pueden estar geo-bloqueados
- Intenta más tarde si YouTube está experimentando problemas

### Video no se descarga
- Verifica que tengas permisos de escritura en la carpeta de descargas
- Asegúrate de tener suficiente espacio en disco
- Algunos videos pueden tener restricciones de descarga

## 📝 Notas técnicas

- Utiliza `yt-dlp` como motor de descarga (sucesor moderno de youtube-dl)
- Los archivos se guardan con nombres seguros (caracteres especiales removidos)
- Solo muestra formatos MP4 con video y audio combinados
- Limita las opciones a las 10 mejores calidades disponibles

## 📄 Licencia

Este proyecto es para uso educativo y personal. Respeta siempre los derechos de autor y términos de servicio de las plataformas de video.
