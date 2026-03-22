from pathlib import Path

DEFAULT_COUNT = 7
DEFAULT_QUALITY = "best"
DEFAULT_OUTPUT_DIR = Path("downloads").resolve()

QUALITY_MAP = {
    "best": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
    "1080": "bestvideo[height<=1080][ext=mp4]+bestaudio/best[height<=1080]",
    "720": "bestvideo[height<=720][ext=mp4]+bestaudio/best[height<=720]",
    "480": "bestvideo[height<=480][ext=mp4]+bestaudio/best[height<=480]",
}
