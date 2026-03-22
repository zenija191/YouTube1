import yt_dlp
from tqdm import tqdm
from pathlib import Path
from .config import QUALITY_MAP, DEFAULT_OUTPUT_DIR
from .utils import sanitize, G, Y, R, RST

class Progress:
    def __init__(self): self.pbar = None
    def __call__(self, d):
        if d['status'] == 'downloading':
            if self.pbar is None:
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                self.pbar = tqdm(total=total, unit='B', unit_scale=True, desc="↓", leave=True)
            self.pbar.update(d.get('downloaded_bytes', 0) - self.pbar.n)
        elif d['status'] == 'finished' and self.pbar:
            self.pbar.close()
            self.pbar = None
            print(f"{G}Файл загружен{RST}")

def download(query: str, count: int, output_dir: Path = DEFAULT_OUTPUT_DIR, quality: str = "best"):
    output_dir.mkdir(parents=True, exist_ok=True)
    fmt = QUALITY_MAP.get(quality, QUALITY_MAP["best"])
    
    print(f"{Y}Качество: {quality}{RST}")
    print(f"Поиск: {query} ({count} видео)")
    print(f"Папка: {output_dir}\n")
    
    ydl_opts = {
        'format': fmt,
        'outtmpl': str(output_dir / '%(title)s.%(ext)s'),
        'noplaylist': True,
        'ignoreerrors': True,
        'continuedl': True,
        'merge_output_format': 'mp4',
        'progress_hooks': [Progress()],
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch{count}:{query}"])
        print(f"\n{G}Готово!{RST}")
    except Exception as e:
        print(f"{R}Ошибка: {e}{RST}")
