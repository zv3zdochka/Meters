import os
import random
import json


class CounterImageSelector:
    def __init__(self, counter_name, base_folder_path=rf"D:\winwin",
                 json_file_path=rf"D:\rename.json"):

        self.counter_name = counter_name
        self.base_folder_path = base_folder_path
        self.json_file_path = json_file_path
        self.image_extensions = {".jpg", ".jpeg", ".png"}

        # Загрузить данные из JSON
        self.counters_data = self.load_json()

        # Найти индекс по имени счетчика
        self.index = self.find_counter_index()

    def load_json(self):
        """Загрузить данные из JSON-файла."""
        with open(self.json_file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def find_counter_index(self):
        """Найти индекс счетчика по его имени в JSON."""
        for index, name in self.counters_data.items():
            if name == self.counter_name:
                return index
        raise ValueError(f"Счетчик с именем '{self.counter_name}' не найден в JSON.")

    def choose_random_image(self):
        """Выбрать случайное фото из папки счетчика и вернуть его путь."""
        # Определить папку по индексу
        counter_folder = os.path.join(self.base_folder_path, self.index)
        if not os.path.exists(counter_folder):
            raise FileNotFoundError(f"Папка для счетчика с индексом '{self.index}' не найдена.")

        # Выбор изображения из папки
        all_files = [
            f for f in os.listdir(counter_folder)
            if
            os.path.isfile(os.path.join(counter_folder, f)) and os.path.splitext(f)[1].lower() in self.image_extensions
        ]

        if not all_files:
            raise FileNotFoundError(f"В папке '{counter_folder}' нет изображений.")

        # Выбираем случайный файл
        chosen_file = random.choice(all_files)

        return os.path.join(counter_folder, chosen_file)


if __name__ == "__main__":
    # Пример использования
    counter_name = "1-10 (100) Ш П1"  # Имя счетчика
    base_folder_path = "/путь/к/вашей/папке"
    json_file_path = "/путь/к/вашему/файлу.json"

    selector = CounterImageSelector(counter_name, base_folder_path, json_file_path)
    selected_image = selector.choose_random_image()
    print(f"Выбранное изображение: {selected_image}")
