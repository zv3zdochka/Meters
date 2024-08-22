from PIL import Image
import json

class ImagePaster:
    def __init__(self, background_image, overlay_images, coordinates_file):
        self.background = background_image
        self.overlay_images = overlay_images
        self.coordinates_file = coordinates_file

    def load_coordinates(self):
        with open(self.coordinates_file, 'r') as file:
            data = json.load(file)
        return data['predictions']

    def paste_images(self):
        coordinates_list = self.load_coordinates()

        for coords in coordinates_list:
            if coords['class'] == 'data':
                overlay = self.overlay_images[0]  # Первое изображение для 'data'
            elif coords['class'] == 'id':
                overlay = self.overlay_images[1]  # Второе изображение для 'id'
            else:
                continue  # Пропускаем если класс не 'data' и не 'id'

            # Получаем размеры для изменения
            width = int(coords['width'] * 0.97)
            height = int(coords['height'] * 0.9)
            overlay_resized = overlay.resize((width, height))

            # Получаем координаты вставки
            x = int(coords['x'])
            y = int(coords['y'])

            # Рассчитываем координаты вставки
            top_left_x = x - width // 2
            top_left_y = y - height // 2

            # Вставляем изображение на фон
            self.background.paste(overlay_resized, (top_left_x, top_left_y), overlay_resized.convert('RGBA'))

        return self.background

    def run(self, output_file):
        result_image = self.paste_images()
        result_image.save(output_file)

# Пример использования
# background_image = Image.open(rf'C:\Users\batsi\PycharmProjects\Meters\dodod\0\1.jpeg')
# overlay_images = [
#     Image.open(rf'C:\Users\batsi\PycharmProjects\Meters\stuff\bar.jpeg'),
#     Image.open(rf'C:\Users\batsi\PycharmProjects\Meters\stuff\id.jpeg')
# ]
# coordinates_file = rf'C:\Users\batsi\PycharmProjects\Meters\dodod\0\1_results.json'
#
# paster = ImagePaster(background_image, overlay_images, coordinates_file)
# paster.run('result.png')
