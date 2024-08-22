from PIL import Image, ImageEnhance
import cv2
import numpy as np


def degrade_image(image_pillow, brightness=0.8, contrast=0.7, blur=9):
    if blur % 2 == 0:
        blur += 1
    # Открываем изображение с помощью Pillow
    image = image_pillow

    # Понижаем яркость
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness)  # Яркость уменьшается на 50%

    # Понижаем контрастность
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast)  # Контрастность уменьшается на 50%

    # Преобразуем изображение в формат numpy для работы с OpenCV
    image = np.array(image)

    # Уменьшаем качество изображения, добавив размытие
    image = cv2.GaussianBlur(image, (blur, blur), 0)

    # Конвертируем изображение обратно в формат Pillow и сохраняем результат
    image = Image.fromarray(image)
    return image


# Пример использования
# degrade_image(rf'C:\Users\batsi\PycharmProjects\Meters\base.jpg', 'output_image.jpg')
