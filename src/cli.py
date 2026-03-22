import sys
from pathlib import Path
import typer
from .downloader import download_videos
from .config import DEFAULT_COUNT, DEFAULT_OUTPUT_DIR

app = typer.Typer(add_completion=False)

@app.command()
def main(
    query: str = typer.Argument(None),
    count: int = typer.Option(DEFAULT_COUNT, "--count", "-n", min=1),
    output: str = typer.Option(None, "--output", "-o")
):
    if query is None:
        print("\n=== yt-search-downloader ===\n")
        query = input("Поисковый запрос: ").strip()
        if not query:
            print("Запрос пустой. Выход.")
            sys.exit(1)
        c = input(f"Количество видео [{DEFAULT_COUNT}]: ").strip()
        count = int(c) if c.isdigit() else DEFAULT_COUNT
        o = input(f"Папка сохранения [downloads]: ").strip()
        output_dir = Path(o).resolve() if o else DEFAULT_OUTPUT_DIR
    else:
        output_dir = Path(output).resolve() if output else DEFAULT_OUTPUT_DIR

    print(f"\nЗапрос: {query}")
    print(f"Количество: {count}")
    print(f"Папка: {output_dir}\n")
    download_videos(query, count, output_dir)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        main.callback(None, DEFAULT_COUNT, None)
    else:
        app()
