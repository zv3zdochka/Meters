import random

from Choser import CounterImageSelector
from Cropper import ImageExtractor
from Extractor import ColorAnalyzer
from Generator import ImageGenerator
from Place import ImagePaster
from Date import remove_date, apply_date
from Low_Quality import degrade_image
from Save import create_folders_and_save_images

class Maker:

    def __init__(self, data: tuple, id, number):
        self.number = id
        self.model = data[0]
        self.id = data[1]
        self.data = data[2]
        self.date = data[3]
        self.number = number
        self.path, self.image, self.data_im, self.id_im = None, None, None, None
        self.image_id, self.data_image = None, None
        self.output = None
        self.output_path = ''
        self.process_name()


    def job(self):
        self.path = self.select_image(self.model)
        self.crop()
        self.generate_image()
        self.place()
        self.rem_date()
        self.quality()
        self.new_date()
        self.save()

    def new_date(self):
        self.output = apply_date(self.output, self.date)

    def rem_date(self):
        print(type(self.output))
        self.output = remove_date(self.output)

    def process_name(self):
        folder_names = [
            "STAR 101",
            "Star 102",
            "ПУЛЬСАР 1Тш-1",
            "ПУЛЬСАР 1ш-1-5",
            "СКАТ 101",
            "СКАТ 102",
            "СКАТ 105",
            "СКАТ 301",
            "СОЭ-52",
            "СОЭИ-5",
            "СЭО-1.12.402",
            "СЭО-1.14.302",
            "ЦЭ6804"
        ]
        for i in folder_names:
            if i in self.model:
                self.model = i
                break



    def place(self):
        self.output = ImagePaster(self.image, [self.data_image, self.id_image],
                                  self.path[:self.path.index('.')] + "_results.json").paste_images()


    def quality(self):
        self.output = degrade_image(self.output)

    def generate_image(self):
        data_colors = self.detect_colors(self.data_im)
        id_colors = self.detect_colors(self.id_im)

        generator = ImageGenerator(data_colors, id_colors)
        self.id_image = generator.generate_image_with_text(self.id.strip())

        self.data_image = generator.create_image_with_text(self.data.strip())

    def detect_colors(self, image):
        analyzer = ColorAnalyzer(image)

        black_color = analyzer.get_black_color()
        white_color = analyzer.get_white_color()
        red_color = analyzer.get_red_color()

        return black_color, white_color, red_color

    def crop(self):
        extractor = ImageExtractor(self.path, self.path[:self.path.index('.')] + "_results.json")
        original_image, cropped_images = extractor.extract_images()
        self.image = original_image
        self.data_im = cropped_images[0]
        self.id_im = cropped_images[1]

    def select_image(self, name: str):
        selector = CounterImageSelector(name)
        return selector.choose_random_image()

    def save(self):
        self.output_path = create_folders_and_save_images(self.number, self.output, self.data_image, self.id_image)

    def get(self):
        self.job()
        return self.output_path
