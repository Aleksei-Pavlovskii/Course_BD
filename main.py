import os
from dotenv import load_dotenv

from src.db_manager import DBManager
from src.hh_api import HeadHunterAPI
from src.utils import create_table, filling_db, filling_db_vacancies, get_user_time

load_dotenv()
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
params = {"host": host, "port": port, "user": user, "password": password}

list_id_company = ["895945", "68587", "2180", "78638", "9116811", "49357", "4181", "1740", "15478", "80"]

def user_interaction():
    # Получение вакансий с HH.ru и заполнение базы данных
    print(get_user_time())
    user_key_word = input('Введите ключевое слово для поиска: ')

    vacancies = HeadHunterAPI()
    list_vacancies = vacancies.get_vacancies(user_key_word)


    # Отбор вакансий по определенным ID
    sort_vacancies = []
    for vacancy in list_vacancies:
        employer = vacancy.get('employer', {})
        company_id = employer.get('id')

        if company_id is not None and str(company_id) in list_id_company:
            sort_vacancies.append(vacancy)


    create_table('course_bd', params)
    filling_db('course_bd', params, sort_vacancies)
    filling_db_vacancies('course_bd', params, sort_vacancies)

    # # Получение данных из базы
    database = DBManager('course_bd', params)

    while True:
        user_answer = input('Вывести список компаний и количество вакансий? Да/Нет ')
        if user_answer.lower() == 'да':
            for company in database.get_companies_and_vacancies_count():
                print(f'Компания: {company[0]}, количество вакансий {company[1]}')
            break
        elif user_answer.lower() =='нет':
            break
        else:
            print('Введите Да или Нет')

    while True:
        user_answer = input('Вывести список всех вакансий? Да/Нет ')
        if user_answer.lower() == 'да':
            for vacancy in database.get_all_vacancies():
                if vacancy[2] != None:
                    print(f'{vacancy[0]}, {vacancy[1]}, зарплата от{vacancy[2]}, {vacancy[3]}')
                else:
                    print(f'{vacancy[0]}, {vacancy[1]}, зарплата не указана, {vacancy[3]}')
            break
        elif user_answer.lower() =='нет':
            break
        else:
            print('Введите Да или Нет')


    avg_salary = database.get_avg_salary()  # среднее значение зарплаты

    while True:
        user_answer = input('Вывести среднюю зарплату? Да/Нет ')
        if user_answer.lower() == 'да':
            print(avg_salary)
            break
        elif user_answer.lower() == 'нет':
            break
        else:
            print('Введите Да или Нет')

    while True:
        user_answer = input('Вывести вакансии где зарплата выше средней? Да/Нет ')
        if user_answer.lower() == 'да':
            for vacansy in database.get_vacancies_with_higher_salary(avg_salary):
                print(f'{vacansy[1]}, {vacansy[2]}, Зарплата от {vacansy[3]} руб., {vacansy[5]}')
            break
        elif user_answer.lower() == 'нет':
            break
        else:
            print('Введите Да или Нет')

    while True:
        user_answer = input('Вывести вакансии где ключевое слово в названии? Да/Нет ')
        if user_answer.lower() == 'да':
            user_key_word = input('Введите ключевое слово для поиска: ')
            if len(user_key_word) > 0:
                if len(database.get_vacancies_with_keyword(key_word=user_key_word)) > 0:
                    for vacancy in database.get_vacancies_with_keyword(key_word=user_key_word):
                        if vacancy[3] == None:
                            print(f'{vacancy[1]}, {vacancy[2]}, зарплата не указана, {vacancy[4]}')
                        else:
                            print(f'{vacancy[1]}, {vacancy[2]}, зарплата от {vacancy[3]}, {vacancy[4]}')
                    break
                else:
                    print('Вакансий по ключевому слову не найдено')
                    break
            else:
                print('Ключевое слово не задано')
        elif user_answer.lower() == 'нет':
            break
        else:
            print('Введите Да или Нет')

if __name__ == '__main__':
    user_interaction()
