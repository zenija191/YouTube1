import os
import subprocess

# --- НАСТРОЙКИ ---
PATH = '/storage/emulated/0/YouTube/yt-search-downloader'
TOKEN = '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'
USER = 'zenija191'
REPO = 'YouTube1'
REMOTE_URL = f'https://{TOKEN}@github.com/{USER}/{REPO}.git'

def run_cmd(cmd):
    try:
        # Добавили подавление лишних запросов
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        # Если ветки нет, просто идем дальше
        if "cannot rename" in str(e.stderr):
            return True
        print(f"❌ Ошибка в: {cmd}\n{e.stderr}")
        return False

def main():
    if not os.path.exists(PATH):
        print("Путь не найден!")
        return
    os.chdir(PATH)

    print("🚀 Начинаю полную очистку и загрузку...")
    
    # Инициализация и настройка
    run_cmd('git init')
    run_cmd(f'git remote remove origin')
    run_cmd(f'git remote add origin {REMOTE_URL}')
    
    # ЗАСТАВЛЯЕМ ГИТ ЗАПОМНИТЬ ТОКЕН (чтобы не просил пароль)
    run_cmd(f'git config credential.helper store')
    
    # Добавление и коммит
    run_cmd('git add .')
    run_cmd('git commit -m "Final auto-push"')
    
    # Пытаемся переименовать в main, если не выйдет - пушим как есть
    run_cmd('git branch -M main')

    print("📤 Отправка файлов (без пароля)...")
    # Пробуем пуш в main, если не выйдет - в master
    try:
        subprocess.run(f'git push -f origin main', shell=True, check=True)
        print("✅ УСПЕХ! Все файлы на GitHub в ветке MAIN.")
    except:
        try:
            subprocess.run(f'git push -f origin master', shell=True, check=True)
            print("✅ УСПЕХ! Все файлы на GitHub в ветке MASTER.")
        except Exception as e:
            print(f"❌ Ошибка при пуше: {e}")

if __name__ == "__main__":
    main()

