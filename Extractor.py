import random

from PIL import Image
import numpy as np
from collections import Counter


class ColorAnalyzer:
    def __init__(self, image):
        self.image = image
        self.image_rgb = self.image.convert('RGB')
        self.image_array = np.array(self.image_rgb)

    def _get_most_common_color(self, color_range, color_index):
        # Flatten the image array and filter by color index
        color_values = self.image_array[:, :, color_index].flatten()
        histogram = Counter(color_values)
        colors_in_range = [color for color in histogram if color_range[0] <= color <= color_range[1]]
        if colors_in_range:
            most_common_color = max(colors_in_range, key=histogram.get)
            return most_common_color
        return None

    def get_black_color(self):
        dark_threshold = 64
        most_common_dark = self._get_most_common_color((0, dark_threshold), color_index=0)
        if most_common_dark is not None:
            return (most_common_dark, most_common_dark, most_common_dark)
        c = random.randrange(0, 50)
        return (c, c, c)

    def get_white_color(self):
        light_threshold = 192
        most_common_light = self._get_most_common_color((light_threshold, 255), color_index=0)
        if most_common_light is not None:
            return (most_common_light, most_common_light, most_common_light)
        c = random.randrange(220, 255)
        return (c, c, c)

    def get_red_color(self):
        # Red channel: 0 - Red, 1 - Green, 2 - Blue
        red_threshold = 128
        most_common_red = self._get_most_common_color((red_threshold, 255), color_index=0)
        if most_common_red is not None:
            return (0, 0, most_common_red)
        c = random.randrange(0, 150)
        return (0, 0, c)


if __name__ == "__main__":
    # Пример использования
    image_path = r'C:\Users\batsi\PycharmProjects\Meters\data\60-31Ш\cropped\0_4.jpeg'  # Замените на путь к вашему изображению
    analyzer = ColorAnalyzer(image_path)

    black_color = analyzer.get_black_color()
    white_color = analyzer.get_white_color()
    red_color = analyzer.get_red_color()

    print(f"Наиболее часто встречающийся черный цвет (RGB): {black_color}")
    print(f"Наиболее часто встречающийся белый цвет (RGB): {white_color}")
    print(f"Наиболее часто встречающийся красный цвет (RGB): {red_color}")
