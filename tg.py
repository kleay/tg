import requests
import random
import string
from time import sleep


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


def submit_web_form(target_account: str, complaint_details: str):
    url = "https://telegram.org/support"

    fake_email = generate_random_email()

    data = {
        'email': fake_email,
        'subject': 'Report abusive account',
        'question': f"""
        Account to investigate: {target_account}
        Type: {'Username' if target_account.startswith('@') else 'User ID'}
        Violation details: {complaint_details}

        This report was generated automatically.
        """,
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
            print(f"✓ Жалоба на {target_account} отправлена (анонимный email: {fake_email})")
            return True
        else:
            print(f"✗ Ошибка формы (код: {response.status_code})")
            return False
    except Exception as e:
        print(f"✗ Ошибка при отправке: {str(e)}")
        return False


def main():
    print("=== Анонимный телеграм репортер ===")

    target_account = input("Введите username (@example) или ID аккаунта: ").strip()
    complaint_details = input("Опишите нарушение: ").strip()

    try:
        num_complaints = int(input("Введите количество жалоб для отправки (1-1000): ").strip())
        num_complaints = max(1, min(1000, num_complaints))
    except ValueError:
        print("Некорректный ввод, установлено значение по умолчанию (3)")
        num_complaints = 3

    print(f"\nНачата отправка {num_complaints} жалоб...\n")

    success_count = 0
    for i in range(1, num_complaints + 1):
        print(f"Попытка отправки #{i}")
        if submit_web_form(target_account, complaint_details):
            success_count += 1
        sleep(random.uniform(2, 5))

    print(f"\nРезультат: {success_count} из {num_complaints} жалоб успешно отправлены")


if __name__ == "__main__":
    main()