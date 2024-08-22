import os
from PIL import Image


def create_folders_and_save_images(number, base, stick, data):
    folder1 = f"D:\Meters\main"
    folder2 = f"D:\Meters\sub"

    # Создаем папки, если их еще нет
    os.makedirs(folder1, exist_ok=True)
    os.makedirs(folder2, exist_ok=True)

    main_image = base

    main_image.save(os.path.join(folder1, f"{number}.jpg"))
    main_image.save(os.path.join(folder2, f"{number}.jpg"))

    secondary_image1 = stick
    secondary_image2 = data

    # Сохраняем вторичные изображения только в папке 2
    secondary_image1.save(os.path.join(folder2, f"{number}_stick.jpg"))
    secondary_image2.save(os.path.join(folder2, f"{number}_data.jpg"))

    return os.path.join(folder1, f"{number}.jpg")

# # Пример использования
# number = input("Введите номер: ")
# create_folders_and_save_images(number)
