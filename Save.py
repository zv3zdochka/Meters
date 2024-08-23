import os
from PIL import Image


def create_folders_and_save_images(number, base, stick, data, preused):
    folder1 = r"D:\Meters\main"
    folder2 = r"D:\Meters\sub"

    # Создаем папки, если их еще нет
    os.makedirs(folder1, exist_ok=True)
    os.makedirs(folder2, exist_ok=True)

    # Создаем папку с лицевым счетом в folder2
    account_folder = os.path.join(folder2, number)
    os.makedirs(account_folder, exist_ok=True)

    main_image = base
    previous_image = preused
    secondary_image1 = stick
    secondary_image2 = data

    # Сохраняем изображение в главной папке
    main_image.save(os.path.join(folder1, f"{number}.jpg"))

    # Сохраняем изображения в папке с лицевым счетом в folder2
    main_image.save(os.path.join(account_folder, f"{number}.jpg"))
    secondary_image1.save(os.path.join(account_folder, f"{number}_stick.jpg"))
    secondary_image2.save(os.path.join(account_folder, f"{number}_data.jpg"))
    previous_image.save(os.path.join(account_folder, f"{number}_previous.jpg"))

    return os.path.join(folder1, f"{number}.jpg")

# Пример использования:
# number = "123456"
# base = Image.open("base.jpg")
# stick = Image.open("stick.jpg")
# data = Image.open("data.jpg")
# preused = Image.open("previous.jpg")
# create_folders_and_save_images(number, base, stick, data, preused)
