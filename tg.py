import random
import string
import requests
import certifi
from urllib.parse import urlsplit
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Проверка поддержки SOCKS
try:
    from requests.packages.urllib3.contrib.socks import SOCKSProxyManager

    SOCKS_SUPPORT = True
except ImportError:
    SOCKS_SUPPORT = False

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import os
import sys

if sys.platform == 'win32':
    os.environ["PYTHON_SOCKS_PROXY_DEBUG"] = "1"  # Включаем дебаг
    os.environ["DNS_QUERY_TIMEOUT"] = "10"        # Увеличиваем таймаут DNS


def generate_random_email():
    domains = ["gmail.com", "hotmail.com", "mail.ru"]
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{name}@{random.choice(domains)}"


def generate_random_phone_number():
    prefixes = ['+7', '+380', '+1', '+10', '+4']
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


def is_valid_proxy(proxy):
    try:
        parsed = urlsplit(proxy)
        if not parsed.hostname or not parsed.port:
            return False

        # Проверка поддержки SOCKS
        if parsed.scheme == 'socks5' and not SOCKS_SUPPORT:
            print("[!] Для использования SOCKS прокси установите зависимости: pip install requests[socks]")
            return False

        return True
    except:
        return False


def load_proxies_from_file(file_path):
    proxies = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                if not line.startswith(('http://', 'https://', 'socks5://')):
                    line = 'http://' + line

                if is_valid_proxy(line):
                    proxies.append(line)
                else:
                    print(f"[!] Некорректный прокси пропущен: {line}")

        print(f"\nУспешно загружено прокси: {len(proxies)}")
        return proxies

    except Exception as e:
        print(f"[!] Ошибка загрузки прокси: {str(e)}")
        return []


def send_reports(nickname, violation_type, proxies_list, num_requests):
    message = generate_complaint(nickname, violation_type)

    print("\nИспользуемое сообщение для жалоб:")
    print("-" * 50)
    print(message)
    print("-" * 50 + "\n")

    url = "https://telegram.org/support?setln=ru"
    subject = "Жалоба на пользователя"

    use_proxies = len(proxies_list) > 0
    if use_proxies:
        print(f"Используется прокси: {len(proxies_list)} шт.")
    else:
        print("Работа без прокси")

    print(f"\nНачинаем отправку {num_requests} жалоб...")

    for i in range(num_requests):
        try:
            email = generate_random_email()
            phone = generate_random_phone_number()
            user_agent = generate_user_agent()

            proxies = None
            proxy = None
            if use_proxies:
                proxy = random.choice(proxies_list)
                proxies = {'http': proxy, 'https': proxy}

            payload = {
                "subject": subject,
                "message": message,
                "email": email,
                "phone": phone
            }

            response = requests.post(
                url,
                data=payload,
                headers={"User-Agent": user_agent},
                proxies=proxies,
                verify=certifi.where(),
                timeout=15
            )

            status = f"Статус {response.status_code}"
            proxy_info = f"Прокси: {proxy}" if use_proxies else ""
            print(f"Жалоба #{i + 1}: {status} | Email: {email} | Телефон: {phone} {proxy_info}")

        except Exception as e:
            print(f"[!] Ошибка: {str(e)}")
            if "SOCKS" in str(e) and not SOCKS_SUPPORT:
                print("[!] Установите зависимости: pip install requests[socks]")

    print("\nВсе жалобы обработаны!")


if __name__ == '__main__':
    print("=== Telegram Account Reporter ===")

    nickname = input("Введите никнейм нарушителя: ").strip()
    violation_type = input("Введите тип нарушения (SPAM/SCAM/ABUSE/COPYRIGHT): ").strip().upper()

    while True:
        try:
            num_requests = int(input("Введите количество жалоб (по умолчанию 100): ") or 100)
            if num_requests <= 0:
                raise ValueError
            break
        except ValueError:
            print("Ошибка: введите положительное целое число!")

    proxy_file = input("Введите путь к файлу с прокси (оставьте пустым если не нужно): ").strip()
    proxies_list = load_proxies_from_file(proxy_file) if proxy_file else []

    if proxy_file and not proxies_list:
        print("[!] Внимание: прокси не были загружены, работаем без прокси")

    send_reports(
        nickname=nickname,
        violation_type=violation_type,
        proxies_list=proxies_list,
        num_requests=num_requests
    )

    input("\nНажмите Enter для выхода...")