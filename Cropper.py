import os
import json
from PIL import Image


class ImageExtractor:
    def __init__(self, image_path, json_path):
        self.image_path = image_path
        self.json_path = json_path

    def extract_images(self):
        # Проверка наличия изображения и JSON файла
        if not os.path.exists(self.image_path):
            raise FileNotFoundError(f"Image not found at {self.image_path}")
        if not os.path.exists(self.json_path):
            raise FileNotFoundError(f"JSON not found at {self.json_path}")

        image = Image.open(self.image_path)

        with open(self.json_path, 'r') as f:
            data = json.load(f)
            predictions = data.get("predictions", [])

        if len(predictions) != 2:
            raise Exception(f"Some objects are not detected on the image.")

        cropped_images = []

        # Вырезка каждой области, описанной в predictions
        for pred in predictions:
            x = pred['x']
            y = pred['y']
            width = pred['width']
            height = pred['height']

            # Вычисление координат (лево, верх, право, низ)
            left = x - width / 2
            top = y - height / 2
            right = x + width / 2
            bottom = y + height / 2

            cropped_image = image.crop((left, top, right, bottom))
            cropped_images.append(cropped_image)

        return image, cropped_images
#
#
# if __name__ == "__main__":
#     # Пример использования
#     image_path = r"path_to_your_image.jpeg"
#     json_path = r"path_to_your_json.json"
#
#     extractor = ImageExtractor(image_path, json_path)
#     original_image, cropped_images = extractor.extract_images()
#
# # Теперь вы можете работать с оригинальным изображением и двумя обрезанными изображениями, не сохраняя их на диск.
