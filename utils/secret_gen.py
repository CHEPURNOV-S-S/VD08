# utils/secret_gen.py
import secrets

def generate_secret():
    """Генерирует готовый SECRET_KEY для .env"""
    key = secrets.token_urlsafe(32)
    print(f"\nSECRET_KEY={key}\n")
    print("Добавьте эту строку в ваш .env файл.")


if __name__ == "__main__":
    generate_secret()