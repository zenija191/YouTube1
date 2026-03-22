import sys
from pathlib import Path
import yt_dlp
from tqdm import tqdm

# Настройки
DEFAULT_COUNT = 7
DEFAULT_QUALITY_IDX = 1  # 1 = best
DEFAULT_OUTPUT_DIR = Path("downloads")

QUALITY_OPTIONS = [
    ("best",   "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"),
    ("1080p",  "bestvideo[height<=1080][ext=mp4]+bestaudio/best[height<=1080]"),
    ("720p",   "bestvideo[height<=720][ext=mp4]+bestaudio/best[height<=720]"),
    ("480p",   "bestvideo[height<=480][ext=mp4]+bestaudio/best[height<=480]"),
]

def sanitize(name: str) -> str:
    import re
    name = re.sub(r'[^\w\s\-.(),]', '', name.strip())
    return re.sub(r'\s+', '_', name)[:220]

def color(code): return f"\033[{code}m"
G = color(32); Y = color(33); R = color(31); RST = color(0)

class Progress:
    def __init__(self): self.pbar = None
    def __call__(self, d):
        if d['status'] == 'downloading':
            if not self.pbar:
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                self.pbar = tqdm(total=total, unit='B', unit_scale=True, desc="Скачиваю", leave=True)
            self.pbar.update(d.get('downloaded_bytes', 0) - self.pbar.n)
        elif d['status'] == 'finished' and self.pbar:
            self.pbar.close(); self.pbar = None
            print(f"{G}Готово{RST}")

def clean_part_files(output_dir: Path):
    """Переименовывает .part файлы, если они уже завершены"""
    for file in output_dir.glob("*.mp4.part"):
        original = file.with_suffix('.mp4')
        if original.exists():
            # если оригинал уже есть — удаляем .part (неполный)
            file.unlink()
        else:
            # переименовываем .part → .mp4
            file.rename(original)
            print(f"{G}Переименован: {original.name}{RST}")

def download(query, count, out_dir, quality_fmt):
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"{Y}Качество: {quality_fmt.split('[')[0]}{RST}")
    print(f"Поиск: {count} видео → {query}")
    print(f"Папка: {out_dir}\n")

    ydl_opts = {
        'format': quality_fmt,
        'outtmpl': str(out_dir / '%(title)s.%(ext)s'),
        'noplaylist': True,
        'ignoreerrors': True,
        'continuedl': True,
        'no-part': False,  # оставляем .part во время скачивания
        'merge_output_format': 'mp4',
        'progress_hooks': [Progress()],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch{count}:{query}"])
        print(f"\n{G}Скачивание завершено!{RST}")
        
        # После скачивания чистим .part
        clean_part_files(out_dir)
        print(f"{G}Все файлы проверены и переименованы (если нужно){RST}")
    except Exception as e:
        print(f"{R}Ошибка: {e}{RST}")
        # на всякий случай чистим после ошибки
        clean_part_files(out_dir)

if __name__ == "__main__":
    print(f"\n{G}yt-search-downloader{RST} — скачивание видео с YouTube\n")

    query = input("Поисковый запрос: ").strip()
    if not query:
        print(f"{R}Запрос пустой. Выход.{RST}")
        sys.exit(1)

    cnt_str = input(f"Количество видео [{DEFAULT_COUNT}]: ").strip()
    count = int(cnt_str) if cnt_str.isdigit() else DEFAULT_COUNT

    print("\nВыберите качество (цифрой):")
    for i, (label, _) in enumerate(QUALITY_OPTIONS, 1):
        print(f"  {i}) {label}")
    q_idx_str = input(f"Ваш выбор [{DEFAULT_QUALITY_IDX}]: ").strip()
    try:
        q_idx = int(q_idx_str) if q_idx_str else DEFAULT_QUALITY_IDX
        if not 1 <= q_idx <= len(QUALITY_OPTIONS):
            q_idx = DEFAULT_QUALITY_IDX
    except ValueError:
        q_idx = DEFAULT_QUALITY_IDX
    quality_label, quality_fmt = QUALITY_OPTIONS[q_idx - 1]

    folder = input(f"Папка сохранения [downloads]: ").strip()
    out_dir = Path(folder).resolve() if folder else DEFAULT_OUTPUT_DIR

    print(f"\n{Y}→ Запрос: {query}")
    print(f"  Количество: {count}")
    print(f"  Качество: {quality_label}")
    print(f"  Папка: {out_dir}{RST}\n")

    download(query, count, out_dir, quality_fmt)
