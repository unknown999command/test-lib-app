import lib
from datetime import datetime

# Приветственное сообщение для пользователя
print('--------------------------------\n')
print('Приветствую вас в приложении для хранения данных нашей бибилиотеки')
print('Используйте "/add Название, Автор, Год" - для добавления книги')
print('Используйте "/del Номер книги" - для удаления книги')
print('Используйте "/find Название, автор или год написания" - для поиска книги')
print('Используйте "/show" - для отображения всех книг')
print('Используйте "/status Номер книги, новый статус" - для изменения статуса книги')
print('            ("В наличии", "Выдана")')
print('Используйте "/exit" - для выхода из программы\n')
print('--------------------------------\n')

# Загружает базу библиотеки
# hueta
data = lib.load()

def main():
    while True:
        user_input = input("Введите ваш запрос: ")
        if user_input == '/exit':
            print("Работа с базой библиотеки завершена!")
            break
        result = processed_string(user_input) # Обработка запроса пользователя
        print (result)

# Функция для обработки запроса пользователя        
def processed_string(user_input):
    
    if user_input.startswith('/add'):
        values = [value.strip() for value in user_input[5:].split(",")] # Вытаскиваем из строки данные, которые требуются для добавления книги
        if len(values) == 3:  # Убедимся, что строка содержит три части
            title, author, year = values
        else:
            return 'Вы где-то допустили ошибку, проверьте еще раз. Пример правильного запроса "/add Преступление и наказание, Достоевский, 1866"'
        result = addbook(title, author, year)
        return result
    
    if user_input.startswith('/del'): # Код для удаления
        book_id = user_input[5:].strip() # Вытаскиваем из запроса ID книги
        result = delbook(book_id)
        return result
    
    if user_input.startswith('/find'):
        result = findbook(user_input[6:])
        return result
    
    if user_input.startswith('/show'):
        result = showbook()
        return result
    
    if user_input.startswith('/status'):
        values = [value.strip() for value in user_input[8:].split(",")] # Вытаскиваем из строки данные, которые требуются для изменения статуса
        if len(values) == 2:  # Убедимся, что строка содержит две части
            book_id, status = values
        else:
            return 'Вы где-то допустили ошибку, проверьте еще раз. Пример правильного запроса "/status 1, Выдана"'
        result = bookstatus(book_id, status)
        return result
    
    return 'Ошибка, ваш запрос не распознан'

def addbook(title, author, year):
    if year.isdigit() and int(year) <= int(datetime.now().year):
        data['last_id'] = data['last_id'] + 1 # Узнаем последний ид в библиотеки, чтобы сгенерировать иникальный
        data['books'].append({'id': data['last_id'], 'title': str(title), 'author': str(author), 'year': int(year), 'status': 'В наличии'})
        lib.save(data)
        return "Книга добавлена"
    return 'Ошибка, неверно указан год'

def delbook(id):
    if id.isdigit():
        book_for_delete = next((book for book in data['books'] if book['id'] == int(id)), None) # Ищем книгу по ид в базе
        if book_for_delete:
            data['books'].remove(book_for_delete)
            lib.save(data)
            return 'Книга успешно удалена'
        return 'Книги с таким номером не существует'
    return 'Пожалуйста, введите номер книги для удаления'

def showbook():
    result = ''
    for book in data['books']:
        result = result + f'\nНомер книги: {book["id"]} | Название: {book["title"]} | Автор: {book["author"]} | Год: {book["year"]} | Статус: {book["status"]}'
    if result == '':
        return 'Книг в библиотеке не найдено'
    return result

def bookstatus(book_id, status):
    if book_id.isdigit():
        book_for_status = next((book for book in data['books'] if book['id'] == int(book_id)), None) # Ищем книгу по ид в базе
        if book_for_status:
            if status == 'В наличии' or status == 'Выдана':
                book_for_status['status'] = status
                lib.save(data)
                return f'Статус книги успешно изменен на "{status}"'
            return 'Неверно введен статус'
        return 'Книги с таким номером не найдено'
    return 'Неверно введен запрос, номер книги и статус должны быть цифрами'

def findbook(pattern):
    result = ''
    count = 0
    for book in data['books']:
        if pattern.lower() in book['title'].lower() or pattern.lower() in book['author'].lower() or pattern.lower() in str(book['year']).lower(): # Проверка на совпадение в полях книги
            result = result + f'Номер книги: {book["id"]} | Название: {book["title"]} | Автор: {book["author"]} | Год: {book["year"]} | Статус: {book["status"]}\n'
            count += 1
    result = f'Найдено: {count}\n{result}' if result != '' else 'Нет совпадений'
    return result

# Запуск программы
main()