import random

import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
from Low_Quality import degrade_image

class ImageGenerator:
    def __init__(self, colors_data, colors_id, width=600, height=400):
        self.id_c = colors_id
        self.data_c = colors_data
        self.width = width
        self.height = height

    def generate_image_with_text(self, text):
        black = tuple(int(c) for c in self.id_c[0])
        white = tuple(int(c) for c in self.id_c[1])
        if len(text) < 20:
            k = 9
        else:
            k = 8


        image = np.ones((self.height, self.width, 3), dtype=np.uint8) * np.array(white, dtype=np.uint8)

        image_pil = Image.fromarray(image)
        draw = ImageDraw.Draw(image_pil)

        font = ImageFont.truetype("arial.ttf", 32)

        draw.text((100, 270), f"№" + text, font=font, fill=black)
        x0 = 100
        image = np.array(image_pil)
        x0 += len(text) * 20
        # Генерация случайного штрих-кода (вертикальные линии)
        np.random.seed(0)
        l = 0
        for x in range(100, 10000, 8):
            h = np.random.choice([2, 2, 2, 2, 3, 3, 3])

            x0 -= h
            x0 -= k
            if x0 < 0:
                break

            black = tuple(int(c) for c in black)

            try:

                cv2.line(image, (x, 200), (x, 250), black, int(h))
            except Exception as e:
                print(f"Error: {e}")

            l = x
        l += 25

        alpha = 0.9
        image = cv2.convertScaleAbs(image, alpha=alpha, beta=0)

        crop_top_left = (70, 170)
        print(l)
        crop_bottom_right = (l, 320)
        cropped_image = image[crop_top_left[1]:crop_bottom_right[1], crop_top_left[0]:crop_bottom_right[0]]
        image_pil = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
        im = degrade_image(image_pil, brightness=0.9, contrast=0.9, blur=3)
        return im

    @staticmethod
    def draw_text_with_background(image, text, org, font, font_scale, font_color, thickness, bg_color=None):
        (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
        baseline += thickness
        x, y = org

        if bg_color:
            if bg_color == 'from_image':
                sub_img = image[y - text_height - baseline:y + baseline, x:x + text_width]
                bg_color = cv2.mean(sub_img)[:3]
                bg_color = tuple(map(int, bg_color))
            cv2.rectangle(image, (x, y - text_height - baseline), (x + text_width, y + baseline), bg_color, cv2.FILLED)

        font_color = tuple(int(c) for c in font_color)

        cv2.putText(image, text, (x, y), font, font_scale, font_color, thickness)

    def create_image_with_text(self, text):
        height, width = 500, 500
        image = np.zeros((height, width, 3), dtype=np.uint8)

        black = tuple(int(c) for c in self.data_c[0])
        white = tuple(int(c) for c in self.data_c[1])
        red = tuple(int(c) for c in self.data_c[2])
        print(red)
        if len(text) == 5:
            k = 80
        else:
            k = 40
        text = ' '.join(text[i:i+1] for i in range(0, len(text), 1))
        print(text)
        for i in range(height):
            for j in range(width):
                shade = int(black[0])
                image[i, j] = (
                    shade + np.random.randint(-5, 5), shade + np.random.randint(-5, 5),
                    shade + np.random.randint(-5, 5))

        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = 2
        thickness = 3

        (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
        baseline += thickness

        top_left = (100, 100)
        bottom_right = (400, 400)

        text_x = (top_left[0] + bottom_right[0] - text_width) // 2
        text_y = (top_left[1] + bottom_right[1] + text_height) // 2

        self.draw_text_with_background(image, text[:-1], (text_x, text_y), font, font_scale, white, thickness)

        last_char = text[-2:]
        first_char = text[0]
        (first_char_w, first_char_h), _ = cv2.getTextSize(first_char, font, font_scale, thickness)
        first_char_x = text_x + text_width - first_char_w

        (last_char_width, last_char_height), _ = cv2.getTextSize(last_char, font, font_scale, thickness)
        last_char_x = text_x + text_width - last_char_width

        last_char_bg_top_left = (last_char_x + 13, text_y - last_char_height - baseline)
        last_char_bg_bottom_right = (last_char_x + last_char_width, text_y + baseline)
        try:
            cv2.rectangle(image, last_char_bg_top_left, last_char_bg_bottom_right, red, cv2.FILLED)
        except Exception as e:
            print(red)
            print(e)
        cv2.putText(image, last_char, (last_char_x, text_y), font, font_scale, white, thickness)

        line_count = 10
        line_spacing = (last_char_bg_bottom_right[1] - last_char_bg_top_left[1]) // (line_count * 2)
        line_length = 7
        last = 0
        for i in range(11):
            start_y = last_char_bg_top_left[1] + i * 2 * line_spacing + 3
            cv2.line(image, (last_char_bg_bottom_right[0] - line_length + 7, start_y),
                     (last_char_bg_bottom_right[0] + 7, start_y),
                     (190, 190, 190), thickness)
            last = last_char_bg_bottom_right[0] + 7

        crop_top_left = (k, 215)
        crop_bottom_right = (last, 290)
        cropped_image = image[crop_top_left[1]:crop_bottom_right[1], crop_top_left[0]:crop_bottom_right[0]]

        image_pil = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
        im = degrade_image(image_pil, brightness=0.9, contrast=0.9, blur=3)

        return im

#
# if __name__ == "__main__":
#     generator = ImageGenerator(((36, 36, 36), (196, 196, 196), (71, 0, 0)), ((62, 62, 62), (234, 234, 234), (117, 0, 0)))
#
#     text = "2018г. №0603580"
#
#     # result_image = generator.generate_image_with_text(text)
#     # result_image.show()
#
#     text = "12346"
#
#     red = generator.create_image_with_text(text)
#     red.show()