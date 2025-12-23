from typing import Any

import psycopg2


class DBManager:
    """Класс для подключения к базе данных"""

    def __init__(self, db_name: str, params: dict) -> None:
        self.db_name = db_name
        self.params = params.copy()
        self.params["dbname"] = db_name
        self.conn = psycopg2.connect(**self.params)

    def __del__(self) -> None:
        self.conn.close()

    def get_companies_and_vacancies_count(self) -> Any:
        """Получает список всех компаний и количество вакансий у каждой компании"""
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT companies.name, COUNT(*) AS vacancies_count
                FROM companies
                LEFT JOIN vacancies ON companies.company_id = vacancies.company_id
                GROUP BY companies.company_id
                ORDER BY vacancies_count DESC;
                """
            )
            return cur.fetchall()

    def get_all_vacancies(self) -> Any:
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT companies.name, vacancies.name, vacancies.salary_from, vacancies.url
                FROM companies
                LEFT JOIN vacancies ON companies.company_id = vacancies.company_id
                """
            )
            return cur.fetchall()

    def get_avg_salary(self) -> float:
        """Получает среднюю зарплату по вакансиям"""
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT AVG(salary_from)
                FROM vacancies
                WHERE salary_from <> 0
                """
            )
            avg_salary = cur.fetchall()
            return round(float(avg_salary[0][0]), 2)

    def get_vacancies_with_higher_salary(self, avg_salary: float) -> Any:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute(
                f"""SELECT * 
                FROM vacancies
                WHERE salary_from > {avg_salary}
                """
            )
            return cur.fetchall()

    def get_vacancies_with_keyword(self, key_word: str) -> Any:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT * 
                FROM vacancies
                WHERE LOWER(name) LIKE %s""",
                (f"%{key_word.lower()}%",),
            )
            return cur.fetchall()
