#!/usr/bin/env python3
"""
YouTube Video Downloader - GUI Version
Interfaz gráfica para descargar videos de YouTube
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
import re
from pathlib import Path
import sys

try:
    import yt_dlp
except ImportError:
    messagebox.showerror("Error", "yt-dlp no está instalado.\nInstala con: pip install yt-dlp")
    sys.exit(1)

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Variables
        self.download_path = Path("downloads")
        self.download_path.mkdir(exist_ok=True)
        self.video_info = None
        self.formats = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="🎥 YouTube Video Downloader", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # URL input
        ttk.Label(main_frame, text="URL del video:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=50)
        self.url_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=5)
        
        # Botón para obtener info
        self.info_button = ttk.Button(main_frame, text="Obtener Info", 
                                     command=self.get_video_info_thread)
        self.info_button.grid(row=1, column=2, padx=(5, 0), pady=5)
        
        # Frame para información del video
        info_frame = ttk.LabelFrame(main_frame, text="Información del Video", padding="10")
        info_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        info_frame.columnconfigure(1, weight=1)
        
        # Labels de información
        ttk.Label(info_frame, text="Título:").grid(row=0, column=0, sticky=tk.W)
        self.title_label = ttk.Label(info_frame, text="", wraplength=400)
        self.title_label.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        ttk.Label(info_frame, text="Canal:").grid(row=1, column=0, sticky=tk.W)
        self.channel_label = ttk.Label(info_frame, text="")
        self.channel_label.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        ttk.Label(info_frame, text="Duración:").grid(row=2, column=0, sticky=tk.W)
        self.duration_label = ttk.Label(info_frame, text="")
        self.duration_label.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Frame para selección de calidad
        quality_frame = ttk.LabelFrame(main_frame, text="Seleccionar Calidad", padding="10")
        quality_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        quality_frame.columnconfigure(0, weight=1)
        
        # Listbox para calidades
        self.quality_listbox = tk.Listbox(quality_frame, height=6)
        self.quality_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Scrollbar para listbox
        scrollbar = ttk.Scrollbar(quality_frame, orient=tk.VERTICAL, command=self.quality_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S), pady=(0, 10))
        self.quality_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Frame para ruta de descarga
        path_frame = ttk.Frame(quality_frame)
        path_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        path_frame.columnconfigure(1, weight=1)
        
        ttk.Label(path_frame, text="Carpeta destino:").grid(row=0, column=0, sticky=tk.W)
        self.path_var = tk.StringVar(value=str(self.download_path.absolute()))
        self.path_entry = ttk.Entry(path_frame, textvariable=self.path_var, state="readonly")
        self.path_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        ttk.Button(path_frame, text="Cambiar", command=self.select_download_path).grid(row=0, column=2, padx=(5, 0))
        
        # Botón de descarga
        self.download_button = ttk.Button(main_frame, text="🔽 Descargar Video", 
                                         command=self.download_video_thread, state="disabled")
        self.download_button.grid(row=4, column=0, columnspan=3, pady=20)
        
        # Barra de progreso
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Label de estado
        self.status_var = tk.StringVar(value="Listo para usar")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=6, column=0, columnspan=3)
    
    def validate_youtube_url(self, url):
        """Valida si la URL es de YouTube"""
        youtube_regex = re.compile(
            r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
            r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        )
        return youtube_regex.match(url) is not None
    
    def get_video_info_thread(self):
        """Ejecuta get_video_info en un hilo separado"""
        threading.Thread(target=self.get_video_info, daemon=True).start()
    
    def get_video_info(self):
        """Obtiene información del video"""
        url = self.url_var.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Por favor ingresa una URL")
            return
        
        if not self.validate_youtube_url(url):
            messagebox.showerror("Error", "La URL no parece ser de YouTube")
            return
        
        # Actualizar UI
        self.root.after(0, lambda: self.status_var.set("Obteniendo información del video..."))
        self.root.after(0, lambda: self.progress.start())
        self.root.after(0, lambda: self.info_button.config(state="disabled"))
        
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Obtener formatos disponibles - solo formatos combinados (sin FFmpeg)
                formats = []
                
                # Buscar SOLO formatos que ya tengan video y audio combinados
                for fmt in info.get('formats', []):
                    if (fmt.get('height') and 
                        fmt.get('vcodec') != 'none' and 
                        fmt.get('acodec') != 'none' and
                        fmt.get('ext') in ['mp4', 'webm']):
                        formats.append({
                            'format_id': fmt['format_id'],
                            'height': fmt['height'],
                            'fps': fmt.get('fps', 30),
                            'filesize': fmt.get('filesize', 0),
                            'quality': f"{fmt['height']}p",
                            'ext': fmt.get('ext', 'mp4'),
                            'type': 'combined'
                        })
                
                # Si no encontramos formatos combinados, usar formatos básicos conocidos
                if len(formats) == 0:
                    # Agregar formatos básicos que siempre funcionan
                    basic_formats = [
                        {'id': '18', 'height': 360, 'quality': '360p (MP4)'},
                        {'id': '22', 'height': 720, 'quality': '720p (MP4)'},
                        {'id': 'best[ext=mp4]', 'height': 480, 'quality': 'Mejor calidad MP4'},
                        {'id': 'worst[ext=mp4]', 'height': 240, 'quality': 'Menor calidad MP4'}
                    ]
                    
                    for fmt_info in basic_formats:
                        formats.append({
                            'format_id': fmt_info['id'],
                            'height': fmt_info['height'],
                            'fps': 30,
                            'filesize': 0,
                            'quality': fmt_info['quality'],
                            'ext': 'mp4',
                            'type': 'basic'
                        })
                
                # Ordenar y eliminar duplicados
                formats.sort(key=lambda x: x['height'], reverse=True)
                seen_heights = set()
                unique_formats = []
                for fmt in formats:
                    if fmt['height'] not in seen_heights:
                        unique_formats.append(fmt)
                        seen_heights.add(fmt['height'])
                
                self.video_info = {
                    'title': info.get('title', 'Video sin título'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Desconocido'),
                    'formats': unique_formats[:10]
                }
                
                # Actualizar UI en el hilo principal
                self.root.after(0, self.update_video_info_ui)
        
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error al obtener información: {str(e)}"))
        
        finally:
            self.root.after(0, lambda: self.progress.stop())
            self.root.after(0, lambda: self.info_button.config(state="normal"))
            self.root.after(0, lambda: self.status_var.set("Listo"))
    
    def update_video_info_ui(self):
        """Actualiza la UI con la información del video"""
        if not self.video_info:
            return
        
        # Actualizar labels
        self.title_label.config(text=self.video_info['title'])
        self.channel_label.config(text=self.video_info['uploader'])
        
        if self.video_info['duration']:
            minutes = self.video_info['duration'] // 60
            seconds = self.video_info['duration'] % 60
            self.duration_label.config(text=f"{minutes}:{seconds:02d}")
        
        # Actualizar listbox de calidades
        self.quality_listbox.delete(0, tk.END)
        self.formats = self.video_info['formats']
        
        for fmt in self.formats:
            filesize_str = self.format_filesize(fmt['filesize'])
            fps_str = f" @ {fmt['fps']}fps" if fmt['fps'] != 'N/A' else ""
            display_text = f"{fmt['quality']}{fps_str} - {filesize_str}"
            self.quality_listbox.insert(tk.END, display_text)
        
        # Habilitar botón de descarga
        self.download_button.config(state="normal")
        self.status_var.set("Video listo para descargar")
    
    def format_filesize(self, size_bytes):
        """Convierte bytes a formato legible"""
        if not size_bytes:
            return "Tamaño desconocido"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def select_download_path(self):
        """Selecciona la carpeta de descarga"""
        folder = filedialog.askdirectory(initialdir=self.download_path)
        if folder:
            self.download_path = Path(folder)
            self.path_var.set(str(self.download_path.absolute()))
    
    def download_video_thread(self):
        """Ejecuta download_video en un hilo separado"""
        threading.Thread(target=self.download_video, daemon=True).start()
    
    def download_video(self):
        """Descarga el video seleccionado"""
        selection = self.quality_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Por favor selecciona una calidad")
            return
        
        selected_format = self.formats[selection[0]]
        url = self.url_var.get().strip()
        
        # Actualizar UI
        self.root.after(0, lambda: self.status_var.set("Descargando video..."))
        self.root.after(0, lambda: self.progress.start())
        self.root.after(0, lambda: self.download_button.config(state="disabled"))
        
        try:
            # Limpiar título para nombre de archivo
            safe_title = re.sub(r'[<>:"/\\|?*]', '_', self.video_info['title'])
            safe_title = safe_title[:100]
            
            output_path = self.download_path / f"{safe_title}.%(ext)s"
            
            # Configurar opciones de descarga
            ydl_opts = {
                'format': selected_format['format_id'],
                'outtmpl': str(output_path),
            }
                
            # Actualizar UI en el hilo principal
            self.root.after(0, self.update_video_info_ui)
        
    except Exception as e:
        self.root.after(0, lambda: messagebox.showerror("Error", f"Error al obtener información: {str(e)}"))
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error durante la descarga: {str(e)}"))
            self.root.after(0, lambda: self.status_var.set("Error en la descarga"))
        
        finally:
            self.root.after(0, lambda: self.progress.stop())
            self.root.after(0, lambda: self.download_button.config(state="normal"))

def main():
    """Función principal"""
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
