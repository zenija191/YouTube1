import os
import subprocess

# --- НАСТРОЙКИ ---
PATH = '/storage/emulated/0/YouTube/yt-search-downloader'
TOKEN = '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'
USER = 'zenija191'
REPO = 'YouTube1'
# Формируем URL с авторизацией, чтобы не спрашивал пароль
REMOTE_URL = f'https://{TOKEN}@github.com/{USER}/{REPO}.git'

def run_cmd(cmd):
    """Функция для запуска команд терминала"""
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {cmd[:20]}... OK")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка в команде: {cmd}")
        print(f"Детали: {e.stderr}")
        return False

def main():
    if not os.path.exists(PATH):
        print(f"Ошибка: Путь {PATH} не найден!")
        return

    os.chdir(PATH)

    # 1. Инициализация если нет .git
    if not os.path.exists('.git'):
        run_cmd('git init')

    # 2. Настройка удаленного репозитория
    run_cmd(f'git remote remove origin') # Удаляем старый на всякий случай
    run_cmd(f'git remote add origin {REMOTE_URL}')

    # 3. Настройка ветки (делаем main основной)
    run_cmd('git branch -M main')

    # 4. Добавление файлов
    print("Индексируем файлы...")
    run_cmd('git add .')

    # 5. Коммит (если есть что коммитить)
    run_cmd('git commit -m "Auto-upload from Android"')

    # 6. Финальный пуш (Force push решает проблему с конфликтами)
    print("Отправка на GitHub (принудительно)...")
    if run_cmd('git push -f origin main'):
        print("\n" + "="*30)
        print("ВСЁ ГОТОВО! Проверяй репозиторий.")
        print(f"https://github.com/{USER}/{REPO}")
        print("="*30)
    else:
        print("\n❌ Что-то пошло не так. Проверь интернет или токен.")

if __name__ == "__main__":
    main()
