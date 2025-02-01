import random
import string
import requests
import certifi
import fake_useragent
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Игнорируем предупреждения о незащищенных запросах
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def generate_random_email():
    domains = ["gmail.com", "hotmail.com","mail.ru"]
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{name}@{random.choice(domains)}"


def generate_random_phone_number():
    prefixes = ['+7', '+380','+1','+10','+4',]
    number = ''.join(random.choices(string.digits, k=10))
    return f"{random.choice(prefixes)}{number}"


def generate_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15",
    ]
    return random.choice(user_agents)


def generate_complaint(nickname, violation_type):
    violations = {
        "SPAM": f"Пользователь {nickname} рассылает массовые рекламные сообщения и спам",
        "SCAM": f"Обнаружена мошенническая деятельность пользователя {nickname}",
        "ABUSE": f"Пользователь {nickname} нарушает правила сообщества грубым поведением",
        "COPYRIGHT": f"Аккаунт {nickname} распространяет контент с нарушением авторских прав",
        "DEFAULT": f"Пользователь {nickname} систематически нарушает правила платформы"
    }

    return violations.get(violation_type.upper(),
                          violations["DEFAULT"]) + ". Прошу принять меры и заблокировать данный аккаунт."


def send_reports(nickname, violation_type, num_requests=100):
    message = generate_complaint(nickname, violation_type)

    print("\nИспользуемое сообщение для жалоб:")
    print("-" * 50)
    print(message)
    print("-" * 50 + "\n")

    url = "https://telegram.org/support?setln=ru"
    subject = "Жалоба на пользователя"

    print(f"Начинаем отправку {num_requests} жалоб...")
    for i in range(num_requests):
        try:
            email = generate_random_email()
            phone = generate_random_phone_number()
            user_agent = generate_user_agent()

            payload = {
                "subject": subject,
                "message": message,
                "email": email,
                "phone": phone
            }

            response = requests.post(url,
                                     data=payload,
                                     headers={"User-Agent": user_agent},
                                     verify=certifi.where())

            print(f"Жалоба #{i + 1}: Статус {response.status_code} | Email: {email} | Телефон: {phone}")

        except Exception as e:
            print(f"Ошибка при отправке запроса: {str(e)}")

    print("\nВсе жалобы успешно отправлены!")


if __name__ == '__main__':
    print("=== Telegram Account Reporter ===")
    nickname = input("Введите никнейм нарушителя: ")
    violation_type = input("Введите тип нарушения (SPAM/SCAM/ABUSE/COPYRIGHT): ")

    send_reports(nickname, violation_type)

    input("\nНажмите Enter для выхода...")