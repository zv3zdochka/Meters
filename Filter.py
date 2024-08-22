import os
import json

# Поддерживаемые форматы изображений
SUPPORTED_IMAGE_EXTENSIONS = [".png", ".jpeg", ".jpg", ".bmp", ".gif"]

# Функция для проверки условий
def check_conditions(predictions):
    data_rects = []
    id_rects = []

    # Сортируем предсказания по классам
    for prediction in predictions:
        if prediction['class'] == 'data':
            data_rects.append(prediction)
        elif prediction['class'] == 'id':
            id_rects.append(prediction)

    # Условие 1: Проверка, что ровно один элемент data и хотя бы один элемент id
    if len(data_rects) != 1 or len(id_rects) > 1:
        return "elems"

    data_rect = data_rects[0]
    if len(id_rects) != 0:
        id_rect = id_rects[0]  # Берем первый элемент id, если их несколько

        # Условие 2: проверка расположения id выше data
        if id_rect['y'] < data_rect['y']:
            return "higher"

    # Условие 3: проверка соотношения ширины и высоты для data
    if data_rect['width'] < data_rect['height'] * 3.5:
        return 'coef'

    return True

# Функция для поиска изображения с любым расширением
def find_image_with_any_extension(base_path):
    for ext in SUPPORTED_IMAGE_EXTENSIONS:
        image_path = f"{base_path}{ext}"
        if os.path.exists(image_path):
            return image_path
    return None

# Функция для удаления файлов, если они не проходят проверку
def process_directory(root_dir):
    # Проходим по всем директориям и файлам
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file in filenames:
            # Ищем JSON файлы
            if file.endswith("_results.json"):
                json_path = os.path.join(dirpath, file)
                base_name = os.path.join(dirpath, file.replace("_results.json", ""))

                # Ищем изображение с любым поддерживаемым расширением
                image_path = find_image_with_any_extension(base_name)

                # Если изображение найдено, проверяем и удаляем, если необходимо
                if image_path:
                    with open(json_path, 'r') as json_file:
                        data = json.load(json_file)
                    print(check_conditions(data.get("predictions", [])))
                    # if not check_conditions(data.get("predictions", [])):
                    #     # Удаляем файлы, если не проходят проверку
                    #     os.remove(json_path)
                    #     os.remove(image_path)
                    #     print(f"Удалено: {json_path} и {image_path}")

# Пример вызова функции
process_directory(r"D:\winwin")
