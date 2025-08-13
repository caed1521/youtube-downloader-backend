#!/usr/bin/env python3
"""
YouTube Video Downloader
Descarga videos de YouTube en formato MP4 con selección de calidad
"""

import os
import sys
import re
from pathlib import Path
try:
    import yt_dlp
except ImportError:
    print("Error: yt-dlp no está instalado.")
    print("Instala con: pip install yt-dlp")
    sys.exit(1)

class YouTubeDownloader:
    def __init__(self):
        self.download_path = Path("downloads")
        self.download_path.mkdir(exist_ok=True)
    
    def validate_youtube_url(self, url):
        """Valida si la URL es de YouTube"""
        youtube_regex = re.compile(
            r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
            r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        )
        return youtube_regex.match(url) is not None
    
    def get_video_info(self, url):
        """Obtiene información del video y formatos disponibles"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Obtener formatos disponibles con mejor calidad
                formats = []
                
                # Primero intentar obtener formatos combinados (video+audio)
                for fmt in info.get('formats', []):
                    if (fmt.get('height') and 
                        fmt.get('vcodec') != 'none' and 
                        fmt.get('acodec') != 'none'):
                        formats.append({
                            'format_id': fmt['format_id'],
                            'height': fmt['height'],
                            'fps': fmt.get('fps', 30),
                            'filesize': fmt.get('filesize', 0),
                            'quality': f"{fmt['height']}p",
                            'type': 'combined'
                        })
                
                # Si no hay suficientes formatos combinados, agregar formatos de video solo
                # (yt-dlp automáticamente combinará con audio)
                if len(formats) < 3:
                    for fmt in info.get('formats', []):
                        if (fmt.get('height') and 
                            fmt.get('vcodec') != 'none' and 
                            fmt.get('acodec') == 'none'):
                            formats.append({
                                'format_id': f"{fmt['format_id']}+bestaudio",
                                'height': fmt['height'],
                                'fps': fmt.get('fps', 30),
                                'filesize': fmt.get('filesize', 0),
                                'quality': f"{fmt['height']}p",
                                'type': 'separate'
                            })
                
                # Ordenar por calidad (altura) descendente
                formats.sort(key=lambda x: x['height'], reverse=True)
                
                # Eliminar duplicados por altura
                seen_heights = set()
                unique_formats = []
                for fmt in formats:
                    if fmt['height'] not in seen_heights:
                        unique_formats.append(fmt)
                        seen_heights.add(fmt['height'])
                
                return {
                    'title': info.get('title', 'Video sin título'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Desconocido'),
                    'formats': unique_formats[:10]  # Limitar a 10 opciones
                }
        
        except Exception as e:
            raise Exception(f"Error al obtener información del video: {str(e)}")
    
    def format_filesize(self, size_bytes):
        """Convierte bytes a formato legible"""
        if not size_bytes:
            return "Tamaño desconocido"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def download_video(self, url, format_id, title):
        """Descarga el video en el formato seleccionado"""
        try:
            # Limpiar el título para el nombre del archivo
            safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
            safe_title = safe_title[:100]  # Limitar longitud
            
            output_path = self.download_path / f"{safe_title}.%(ext)s"
            
            ydl_opts = {
                'format': format_id,
                'outtmpl': str(output_path),
                'noplaylist': True,
                'merge_output_format': 'mp4',  # Asegurar salida en MP4
                'writesubtitles': False,
                'writeautomaticsub': False,
            }
            
            print(f"\n🔄 Descargando: {title}")
            print("=" * 50)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            print(f"\n✅ ¡Descarga completada!")
            print(f"📁 Ubicación: {self.download_path.absolute()}")
            
        except Exception as e:
            raise Exception(f"Error durante la descarga: {str(e)}")
    
    def run(self):
        """Función principal del programa"""
        print("🎥 YouTube Video Downloader")
        print("=" * 40)
        
        while True:
            try:
                # Solicitar URL
                print("\n📎 Ingresa el link del video de YouTube:")
                print("(o escribe 'salir' para terminar)")
                url = input("URL: ").strip()
                
                if url.lower() in ['salir', 'exit', 'quit']:
                    print("👋 ¡Hasta luego!")
                    break
                
                if not url:
                    print("❌ Por favor ingresa una URL válida.")
                    continue
                
                if not self.validate_youtube_url(url):
                    print("❌ La URL no parece ser de YouTube. Intenta de nuevo.")
                    continue
                
                # Obtener información del video
                print("\n🔍 Obteniendo información del video...")
                video_info = self.get_video_info(url)
                
                # Mostrar información del video
                print(f"\n📺 Título: {video_info['title']}")
                print(f"👤 Canal: {video_info['uploader']}")
                if video_info['duration']:
                    minutes = video_info['duration'] // 60
                    seconds = video_info['duration'] % 60
                    print(f"⏱️  Duración: {minutes}:{seconds:02d}")
                
                # Mostrar opciones de calidad
                formats = video_info['formats']
                if not formats:
                    print("❌ No se encontraron formatos MP4 disponibles.")
                    continue
                
                print(f"\n🎬 Calidades disponibles:")
                print("-" * 50)
                for i, fmt in enumerate(formats, 1):
                    filesize_str = self.format_filesize(fmt['filesize'])
                    fps_str = f" @ {fmt['fps']}fps" if fmt['fps'] != 'N/A' else ""
                    print(f"{i}. {fmt['quality']}{fps_str} - {filesize_str}")
                
                # Solicitar selección de calidad
                while True:
                    try:
                        print(f"\n🎯 Selecciona la calidad (1-{len(formats)}):")
                        choice = input("Opción: ").strip()
                        
                        if not choice:
                            continue
                            
                        choice_num = int(choice)
                        if 1 <= choice_num <= len(formats):
                            selected_format = formats[choice_num - 1]
                            break
                        else:
                            print(f"❌ Por favor selecciona un número entre 1 y {len(formats)}")
                    
                    except ValueError:
                        print("❌ Por favor ingresa un número válido.")
                
                # Confirmar descarga
                print(f"\n📥 ¿Descargar en calidad {selected_format['quality']}?")
                confirm = input("Confirmar (s/n): ").strip().lower()
                
                if confirm in ['s', 'si', 'sí', 'y', 'yes']:
                    self.download_video(url, selected_format['format_id'], video_info['title'])
                else:
                    print("❌ Descarga cancelada.")
                
                print("\n" + "="*50)
                
            except KeyboardInterrupt:
                print("\n\n👋 Programa interrumpido por el usuario.")
                break
            
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Intenta con otro video o verifica tu conexión a internet.")

def main():
    """Punto de entrada del programa"""
    try:
        downloader = YouTubeDownloader()
        downloader.run()
    except KeyboardInterrupt:
        print("\n👋 ¡Hasta luego!")
    except Exception as e:
        print(f"Error fatal: {e}")

if __name__ == "__main__":
    main()
