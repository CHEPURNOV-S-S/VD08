# run.py

import os
import sys

if not os.path.exists("config.py"):
    print("❌ Ошибка: файл config.py не найден.")
    print("👉 Чтобы создать его, выполните:")
    print("   cp config_template.py config.py")
    print("Затем откройте config.py и настройте параметры по своему усмотрению.")
    sys.exit(1)

from app import create_app

app = create_app()

if __name__ == '__main__':
    print ("Start app/Запуск приложения")
    app.run()