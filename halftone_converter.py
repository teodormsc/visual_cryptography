import math
from os import mkdir

from PIL import Image
from pathlib import Path

def bayer_matrix(size, matrix):
    current_size = len(matrix)
    if current_size == size:
        return matrix
    else:
        new_size = current_size * 2
        output_matrix = [[0] * new_size for row in range(new_size)]

        for i in range(current_size):
            for j in range(current_size):
                current_element = matrix[i][j]
                output_matrix[i][j] = current_element * 4;
                output_matrix[i][j + current_size] = current_element * 4 + 2
                output_matrix[i + current_size][j] = current_element * 4 + 3
                output_matrix[i + current_size][j + current_size] = current_element * 4 + 1
        return bayer_matrix(size, output_matrix)


def crop_image(image, bayer_size):
    width, height = image.size
    extra_width = width % bayer_size
    extra_height = height % bayer_size
    image = image.crop((0, 0, width - extra_width, height - extra_height))
    return image


class HalftoneConverter:
    def grayscale_bayer_dithering(self, image, bayer_size, output_folder="output", output_name="bayer", is_path=True):
        if bayer_size <= 1 or not math.log2(bayer_size).is_integer():
            print("INVALID BAYER-MATRIX SIZE")
            return

        bayer_base = [[0, 2], [3, 1]]
        bayer = bayer_matrix(bayer_size, bayer_base)

        max_element = max(max(row) for row in bayer)
        bayer = [[element / max_element for element in row] for row in bayer]

        if is_path:
            image = Image.open(image).convert("L")
            image = crop_image(image, bayer_size)
        pixels = image.load()
        new_width, new_height = image.size

        for y in range(new_height):
            for x in range(new_width):
                bayer_value = bayer[y % bayer_size][x % bayer_size]
                normalized_pixel = pixels[x, y] / 255
                if normalized_pixel >= bayer_value:
                    pixels[x, y] = int(255)
                else:
                    pixels[x, y] = int(0)

        path = Path(output_folder)
        path.mkdir(parents=True, exist_ok=True)
        image.save(f"{output_folder}/{output_name}.png")


    def color_bayer_dithering(self, image_path, bayer_size, output_folder="output", red_channel_name="bayer_red",
                              green_channel_name="bayer_green", blue_channel_name="bayer_blue"):
        image = Image.open(image_path)
        image = crop_image(image, bayer_size)
        r, g, b, = image.split()
        self.grayscale_bayer_dithering(r, bayer_size, output_name=red_channel_name, is_path=False)
        self.grayscale_bayer_dithering(g, bayer_size, output_name=green_channel_name, is_path=False)
        self.grayscale_bayer_dithering(b, bayer_size, output_name=blue_channel_name, is_path=False)


    def grayscale_floyd_steinberg_dithering(self, image, output_folder="output", output_name="floyd_steinberg",
                                            is_path=True):
        if (is_path):
            image = Image.open(image).convert("L")
        pixels = image.load()
        width, height = image.size

        for y in range(height):
            for x in range(width):
                old_pixel = pixels[x, y]
                new_pixel = 255 if old_pixel >= 127 else 0
                pixels[x, y] = new_pixel
                error = old_pixel - new_pixel

                if x < width - 1:
                    pixels[x + 1, y] = max(0, min(int(pixels[x + 1, y] + 7 / 16 * error), 255))
                if y < height - 1:
                    if x > 0:
                        pixels[x - 1, y + 1] = max(0, min(int(pixels[x - 1, y + 1] + 3 / 16 * error), 255))
                    pixels[x, y + 1] = max(0, min(int(pixels[x, y + 1] + 5 / 16 * error), 255))
                    if x < width - 1:
                        pixels[x + 1, y + 1] = max(0, min(int(pixels[x + 1, y + 1] + 1 / 16 * error), 255))

        path = Path(output_folder)
        path.mkdir(parents=True, exist_ok=True)
        image.save(f"{output_folder}/{output_name}.png")


    def color_floyd_steinberg_dithering(self, image_path, output_folder="output", red_channel_name="fs_red",
                                        green_channel_name="fs_green", blue_channel_name="fs_blue"):
        image = Image.open(image_path)
        r, g, b = image.split()
        self.grayscale_floyd_steinberg_dithering(r, output_folder, red_channel_name, isPath=False)
        self.grayscale_floyd_steinberg_dithering(g, output_folder, green_channel_name, isPath=False)
        self.grayscale_floyd_steinberg_dithering(b, output_folder, blue_channel_name, isPath=False)




