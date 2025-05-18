import random
from PIL import Image
from pathlib import Path


def fill(pixels, color, i, j):
    pixels[i, j] = color
    pixels[i + 1, j] = 255 - color
    pixels[i, j + 1] = 255 - color
    pixels[i + 1, j + 1] = color


class Encryptor:
    def encrypt_grayscale(self, image_path, output_folder="output", output_one_name="component_one",
                          output_two_name="component_two"):
        image = Image.open(image_path).convert("L")
        pixels = image.load()
        width, height = image.size

        c_one = Image.new("L", (width * 2, height * 2))
        c_two = Image.new("L", (width * 2, height * 2))
        pixels_one = c_one.load()
        pixels_two = c_two.load()

        for y in range(height):
            for x in range(width):
                color = random.choice([0, 255])
                if pixels[x, y] == 255:
                    fill(pixels_one, color, 2 * x, 2 * y)
                    fill(pixels_two, color, 2 * x, 2 * y)
                else:
                    fill(pixels_one, color, 2 * x, 2 * y)
                    fill(pixels_two, 255 - color, 2 * x, 2 * y)

        path = Path(output_folder)
        path.mkdir(parents=True, exist_ok=True)
        c_one.save(f"{output_folder}/{output_one_name}.png")
        c_two.save(f"{output_folder}/{output_two_name}.png")


    def encrypt_color(self, channel_paths, output_folder="output", red_one_name="red_one", red_two_name="red_two",
                      green_one_name="green_one", green_two_name="green_two", blue_one_name="blue_one",
                      blue_two_name="blue_two"):
        self.encrypt_grayscale(channel_paths[0], output_folder, red_one_name, red_two_name)
        self.encrypt_grayscale(channel_paths[1], output_folder, green_one_name, green_two_name)
        self.encrypt_grayscale(channel_paths[2], output_folder, blue_one_name, blue_two_name)








