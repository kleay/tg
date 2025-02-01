import requests
import random
import string
from time import sleep


def generate_random_phone():
    country_codes = ['+1', '+7', '+44', '+49', '+33']
    code = random.choice(country_codes)
    number = ''.join(random.choices('0123456789', k=10))
    return f"{code}{number}"


def generate_random_email():
    username_length = random.randint(6, 12)
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=username_length))
    return f"{username}@gmail.com"


def get_random_headers():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    ]
    return {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://telegram.org/',
        'DNT': str(random.randint(0, 1)),
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }


def submit_web_form(target_phone: str, complaint_details: str):
    url = "https://telegram.org/support"

    fake_email = generate_random_email()
    fake_phone = generate_random_phone()

    data = {
        'email': fake_email,
        'subject': 'Report abusive account',
        'question': f"""
        Account to investigate: {target_phone}
        Violation details: {complaint_details}

        This report was generated automatically.
        """,
        'phone': fake_phone
    }

    try:
        sleep(random.uniform(1, 3))

        response = requests.post(
            url,
            data=data,
            headers=get_random_headers(),
            allow_redirects=False,
            timeout=10
        )

        if response.status_code == 302:
            print(f"✓ Жалоба отправлена (использованы данные: {fake_email}/{fake_phone})")
            return True
        else:
            print(f"✗ Ошибка формы (код: {response.status_code})")
            return False
    except Exception as e:
        print(f"✗ Ошибка при отправке: {str(e)}")
        return False


def main():
    print("=== Анонимный телеграм репортер ===")

    target_phone = input("Введите номер нарушителя (с кодом страны): ").strip()
    complaint_details = input("Опишите нарушение: ").strip()

    try:
        num_complaints = int(input("Введите количество жалоб для отправки (1-100): ").strip())
        num_complaints = max(1, min(100, num_complaints))  # Ограничение от 1 до 10
    except ValueError:
        print("Некорректный ввод, установлено значение по умолчанию (3)")
        num_complaints = 3

    print(f"\nНачата отправка {num_complaints} жалоб...\n")

    success_count = 0
    for i in range(1, num_complaints + 1):
        print(f"Попытка отправки #{i}")
        if submit_web_form(target_phone, complaint_details):
            success_count += 1
        sleep(random.uniform(2, 5))

    print(f"\nРезультат: {success_count} из {num_complaints} жалоб успешно отправлены")


if __name__ == "__main__":
    main()