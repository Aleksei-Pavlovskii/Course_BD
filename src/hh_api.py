import requests

from src.parser import Parser


class HeadHunterAPI(Parser):
    """Класс для работы с API HeadHunter"""

    def __init__(self) -> None:
        self.__url = "https://api.hh.ru/vacancies"  # url HeadHunter для получения вакансий
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params: dict = {"text": "", "page": 0, "per_page": 100}  # параметры для запроса
        self.__vacancies: list[dict] = []  # список в который будем записывать вакансии

    def _connect_to_api(self) -> bool:
        """Подключение к API HeadHunter"""
        try:
            response = requests.get(self.__url)
            response.raise_for_status()  # проверка успешности запроса
            return True
        except requests.exceptions.RequestException as err:
            print(f"Ошибка подключения к API {err}")
            return False

    def get_vacancies(self, keyword: str) -> list[dict]:
        """Получение вакансий по ключевому слову"""
        if not self._connect_to_api():
            raise Exception("Ошибка подключения к API")
        self.__params["text"] = keyword  # ключевое слово по которому будем искать вакансии
        while self.__params.get("page") != 20:  # пока страница не будет равна 20
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)  # делаем запрос
            vacancies = response.json()["items"]  # получаем ответ в формате JSON
            self.__vacancies.extend(vacancies)  # записываем вакансии в список
            self.__params["page"] += 1  # переходим к следующей странице
        return self.__vacancies  # возвращаем список вакансий
