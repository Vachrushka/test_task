import json
import random
import string
from EventTypes import EventType

# Заранее предопределенный список участников
participants_list = ["Alice", "Bob", "Charlie", "David", "Eve"]

# Функция для генерации случайной последовательности символов
def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

# Генерация данных
data = {
    "event_time": "2023-07-24T12:34:56Z",  # Здесь нужно указать дату и время в формате ISO с часовой зоной (UTC)
    "event_type": EventType.PRIVATE.name,
    "event_name": generate_random_string(20),
    "event_members": random.sample(participants_list, random.randint(1, len(participants_list))),
    "event_place": random.choice(["zoom", "telegram", generate_random_string(10)])
}

# Преобразование данных в JSON и запись в файл
with open("data/events.json", "w") as file:
    json.dump(data, file, indent=2)

print("JSON файл успешно создан.")
