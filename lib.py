import json

# Сохранение данных в JSON файл
def save(data):
    try:
        with open('books', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f'Ошибка при сохранении: {e}')

# Чтение данных из JSON файла
def load():
    try:
        with open('books', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print('База не найдена. Создаём новую.')
        return {'books': [], 'last_id': 0}
    except Exception as e:
        print(f'Ошибка при чтении: {e}')
        print('База создана заново')
        return {'books': [], 'last_id': 0}