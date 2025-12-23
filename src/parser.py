from abc import ABC, abstractmethod


class Parser(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def _connect_to_api(self) -> bool: ...

    @abstractmethod
    def get_vacancies(self, keyword: str) -> list[dict]: ...
