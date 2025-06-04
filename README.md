# 🚀 Запуск учебного Flask-приложения локально:
## 📦 Шаг 1: Клонирование репозитория
```bash
# Клонируем репозиторий
git clone https://github.com/CHEPURNOV-S-S/VD08.git 
cd VD08
```
## 🔧 Шаг 2: Создание и активация виртуального окружения
Для Linux / macOS / Windows (через WSL):
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Для Windows (PowerShell):
```Powershell
python.exe -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## 🔐 Шаг 3: Настройка переменных окружения
Создайте файл .env в корне проекта:
Linux / macOS:
```bash
nano ./.env 
```

Для Windows (PowerShell):
```Powershell
# Создаём файл с шаблоном
@'
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///site.db
API_NINJAS_KEY=your_api_key_here
DEBUG=1
'@ | Set-Content -Path .\.env -Encoding UTF8

# Редактируем файлю
notepad .\.env
```

Добавьте следующее содержимое в файл .env

```bash
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///site.db
API_NINJAS_KEY=ваш_api_ключ
```
📌 Примечание: Чтобы получить ключ от API, зарегистрируйтесь на https://api-ninjas.com и возьмите ключ из профиля.

## 🔧️ Шаг 5: инициализация БД
Linux / macOS/:
```bash
python3 -m flask create-db
```

Linux / macOS/Windows:
```bash
python -m flask create-db
```

## ▶️ Шаг 6: Запуск приложения
Linux / macOS:
```bash
python3 ./run.py
```
Windows:
```PowerShell
python.exe run.py
```
После этого перейдите в браузере по адресу:

http://127.0.0.1:5000

📌 Примечание: запуск локального запуска тестировался на WIN10 Powershel и в Kali linux.


# 🚀 Руководство по развёртыванию Flask-приложения на VPS

Это пошаговое руководство поможет развернуть Flask-приложение на сервере под управлением Linux с использованием Gunicorn, Nginx и systemd.

## 🧾 Требования

- Сервер на базе Ubuntu (например, 20.04 или 22.04)
- Установленный Python 3.x
- Установленный Git
- Права `sudo`

---

## Шаг 0: Подготовка сервера:

```bash
# Обновляем список пакетов и обновляем систему
sudo apt update 
sudo apt upgrade -y

#Перезагружаем VPS
sudo reboot
# После  перезагрузил VPS, не смог подключится по ssh к серверу. 
# Помогли команды из виртуальной консоли cloud.ru
sudo cloud-init clean
sudo cloud-init init

# Устанавливаем Python pip, venv, веб-сервер Nginx и систему контроля версий Git
sudo apt install -y python3-pip python3-venv nginx git
```

## 🔐 Шаг 1: Создание пользователя

```bash
# Создаем пользователя flaskuser
sudo adduser flaskuser
sudo usermod -aG sudo flaskuser

# Добавляем www-data в группу flaskuser для совместимости с Nginx
sudo usermod -a -G flaskuser www-data

# Переключаемся на пользователя flaskuser
su flaskuser
# Переходим в домашнюю папку flaskuser
cd
```

---

## 📦 Шаг 2: Клонирование репозитория

```bash
# Клонируем репозиторий
git clone https://github.com/CHEPURNOV-S-S/VD08.git 
cd VD08
```

---

## 🧪 Шаг 3: Настройка виртуального окружения

```bash
# Создаем виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Устанавливаем зависимости
pip install -r requirements.txt
pip install gunicorn
```

---

## 🔑 Шаг 4: Настройка переменных окружения

### Сгенерируйте секретный ключ:

```bash
python3 ./utils/secret_gen.py
```

### Создайте файл окружения:

```bash
sudo nano /etc/systemd/system/flaskapp.env
```

Добавьте следующее содержимое:
!ВАЖНО: БЕЗ ПРОБЕЛОВ И КАВЫЧЕК!
```bash
SECRET_KEY=ваш_сгенерированный_ключ
DATABASE_URL=sqlite:///site.db
API_NINJAS_KEY=ваш_api_ключ
DEBUG=0
```

Установите права доступа:

```bash
sudo chown root:root /etc/systemd/system/flaskapp.env
sudo chmod 600 /etc/systemd/system/flaskapp.env
```

---

## 🗃️ Шаг 5: Инициализация базы данных через systemd

Создайте службу:

```bash
sudo nano /etc/systemd/system/flask-db-init.service
```

Вставьте содержимое:

```ini
[Unit]
Description=Инициализация базы данных Flask
After=network.target

[Service]
Type=oneshot
User=flaskuser
EnvironmentFile=/etc/systemd/system/flaskapp.env
WorkingDirectory=/home/flaskuser/VD08
Environment="PATH=/home/flaskuser/VD08/venv/bin"
ExecStart=/home/flaskuser/VD08/venv/bin/flask create-db

[Install]
WantedBy=multi-user.target
```

Запустите службу:

```bash
sudo systemctl start flask-db-init.service
# Проверьте что база данных была создана
sudo systemctl status flask-db-init.service
# В статусе должно быть сообщение "База данных успешно создана"
```

---

## 🚇 Шаг 6: Настройка службы Flask приложения

Создайте файл службы:

```bash
sudo nano /etc/systemd/system/flaskapp.service
```

Вставьте:

```ini
[Unit]
Description=Gunicorn для Flask-приложения
After=network.target

[Service]
User=flaskuser
Group=flaskuser
WorkingDirectory=/home/flaskuser/VD08
EnvironmentFile=/etc/systemd/system/flaskapp.env
Environment="PATH=/home/flaskuser/VD08/venv/bin"
ExecStart=/home/flaskuser/VD08/venv/bin/gunicorn --workers 3 --bind unix:flaskapp.sock -m 007 wsgi:app
Restart=always
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=gunicorn

[Install]
WantedBy=multi-user.target
```

Примените изменения:

```bash
sudo systemctl daemon-reload
sudo systemctl start flaskapp
sudo systemctl enable flaskapp
```
Проверьте что приложение работает

```bash
 curl --unix-socket /home/flaskuser/VD08/flaskapp.sock http://localhost/
```

Должен загрузится HTML код домашней страницы со случайной цитатой.

---

## 🌐 Шаг 7: Настройка Nginx

Создайте конфигурационный файл:

```bash
sudo nano /etc/nginx/sites-available/flaskapp
```

Вставьте:
!ВАЖНО: не забудьте указать домен или ip адрес сервера вместо "your_server_domain or your_sever_ip"!
```nginx
server {
    listen 80;
    server_name your_server_domain or your_sever_ip;

    proxy_headers_hash_max_size 512;
    proxy_headers_hash_bucket_size 128;


    # Разрешаем загрузку файлов до 20 МБ
    client_max_body_size 20M;

    root /home/flaskuser/VD08;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/flaskuser/VD08/flaskapp.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/flaskuser/VD08/app/static/;
        expires 30d;
    }

    access_log /var/log/nginx/flaskapp.access.log;
    error_log /var/log/nginx/flaskapp.error.log;
}
```

Активируйте сайт и перезапустите Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/flaskapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## ✅ Шаг 8: Проверка работы приложения

Откройте браузер и перейдите по адресу:
http://server_ip

Вы должны увидеть запущенное Flask-приложение.

---

## 📝 Примечания

- Проверьте группы безопасности / сетевые ACL / правила фаервола: порт HTTP (80) должен быть открыт для входящих подключений. 
- Не забудьте заменить `ваш_домен_или_IP` на реальный домен или IP-адрес сервера.
- Если вы используете API от [API-Ninjas](https://api-ninjas.com),  укажите свой ключ в `API_NINJAS_KEY`.
- Количество воркеров в Gunicorn можно изменять в зависимости от числа ядер процессора.
- Все шаги инструкции были проверены на бесплатном VPS-сервере с установленной Ubuntu 22.04 на платформе "cloud.ru"

---

**Удачного деплоя! 🚀**