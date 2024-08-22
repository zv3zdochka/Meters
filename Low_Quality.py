from PIL import Image, ImageEnhance
import cv2
import numpy as np


def degrade_image(image_pillow, brightness=0.8, contrast=0.7, blur=9):
    if blur % 2 == 0:
        blur += 1
    image = image_pillow

    # Понижаем яркость
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness)

    # Понижаем контрастность
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast)

    image = np.array(image)

    # Уменьшаем качество изображения
    image = cv2.GaussianBlur(image, (blur, blur), 0)

    image = Image.fromarray(image)
    return image


# Пример использования
# degrade_image(rf'C:\Users\batsi\PycharmProjects\Meters\base.jpg', 'output_image.jpg')
