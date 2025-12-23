from typing import Iterator

import psycopg2


def create_database(db_name: str, params: dict) -> None:
    """Создание базы данных"""
    conn = None
    try:
        # Подключаемся
        conn = psycopg2.connect(dbname="postgres", **params)
        conn.autocommit = True

        # Формирование запроса
        with conn.cursor() as cur:
            try:
                cur.execute(f"DROP DATABASE IF EXISTS {db_name}")  # Удаляем БД
            finally:
                cur.execute(f"CREATE DATABASE {db_name}")  # Создаем БД
        print(f'База "{db_name}" успешно пересоздана!')

    except psycopg2.Error as e:
        print(f"Ошибка при создании БД: {e}")
        raise

    finally:
        if conn:
            conn.close()  # закрываем соединение


def create_table(db_name: str, params: dict) -> None:
    """Создание таблиц"""
    conn = psycopg2.connect(dbname=db_name, **params)

    # Создание таблицы компаний
    with conn.cursor() as cur:
        cur.execute(
            """CREATE TABLE IF NOT EXISTS companies (
        company_id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        url VARCHAR(255) NOT NULL)
        """
        )

    # Создание таблицы вакансий
    with conn.cursor() as cur:
        cur.execute(
            """CREATE TABLE IF NOT EXISTS vacancies (
        vacancy_id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        url VARCHAR(255) NOT NULL,
        salary_from INTEGER,
        salary_to INTEGER,
        requirements TEXT,
        company_id INTEGER NOT NULL,
        FOREIGN KEY (company_id) REFERENCES companies (company_id)
        )"""
        )
    conn.commit()
    conn.close()


def filling_db(db_name: str, params: dict, list_vac: Iterator) -> None:
    """Функиця, которая заполняет таблицу компаний"""
    conn = psycopg2.connect(dbname=db_name, **params)
    with conn.cursor() as cur:  #
        for item in list_vac:
            # Безопасное получение данных
            employer = item.get("employer", {}) or {}

            company_id = employer.get("id", 1) if employer else None
            company_name = employer.get("name") if employer else None
            company_url = employer.get("url", 1) if employer else None

            cur.execute(
                """INSERT INTO companies (company_id, name, url) 
            VALUES (%s, %s, %s)
            ON CONFLICT (company_id) DO NOTHING""",
                (company_id, company_name, company_url),
            )
    conn.commit()
    conn.close()


def filling_db_vacancies(db_name: str, params: dict, list_vac: Iterator) -> None:
    """Функция, которая заполняет таблицу вакансий"""
    conn = psycopg2.connect(dbname=db_name, **params)
    with conn.cursor() as cur:
        for item in list_vac:
            # Безопасное получение данных
            vacancy_id = item.get("id")
            name = item.get("name")
            url = item.get("alternate_url")

            salary_data = item.get("salary", {}) or {}
            salary_from = salary_data.get("from") if salary_data else None
            salary_to = salary_data.get("to") if salary_data else None

            snippet = item.get("snippet", {}) or {}
            requirements = snippet.get("requirement") if snippet else None

            employer = item.get("employer", {}) or {}
            company_id = employer.get("id") if employer else None

            cur.execute(
                """INSERT INTO vacancies 
                   (vacancy_id, name, url, salary_from, salary_to, requirements, company_id) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)
                   ON CONFLICT (vacancy_id) DO NOTHING""",
                (vacancy_id, name, url, salary_from, salary_to, requirements, company_id),
            )
    conn.commit()
    conn.close()
