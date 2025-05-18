from PIL import Image
from pathlib import Path


def remove_noise(pixels, width, height):
    denoised_image = Image.new("L", (int(width / 2), int(height / 2)))
    denoised_pixels = denoised_image.load()

    for y in range(int(height / 2)):
        for x in range(int(width / 2)):
            if pixels[2 * x, 2 * y] != pixels[2 * x + 1, 2 * y]:
                denoised_pixels[x, y] = 255
            else:
                denoised_pixels[x, y] = 0

    return denoised_image


class Decryptor:
    def decrypt_grayscale(self, component_paths, output_folder = "output", output_name="decrypted", store_result=True):
        c_one = Image.open(component_paths[0]).convert("L")
        c_two = Image.open(component_paths[1]).convert("L")
        pixels_one = c_one.load()
        pixels_two = c_two.load()
        width, height = c_one.size

        decrypted_image = Image.new("L", (width, height))
        decrypted_pixels = decrypted_image.load()

        for y in range(height):
            for x in range(width):
                decrypted_pixels[x, y] = min(pixels_one[x, y], pixels_two[x, y])

        decrypted_image = remove_noise(decrypted_pixels, width, height)

        if store_result:
            path = Path(output_folder)
            path.mkdir(parents=True, exist_ok=True)
            decrypted_image.save(f"{output_folder}/{output_name}.png")

        return decrypted_image


    def decrypt_color(self, component_paths, output_folder="output", output_name="decrypted"):
        red_channel = self.decrypt_grayscale([component_paths[0], component_paths[1]])
        green_channel = self.decrypt_grayscale([component_paths[2], component_paths[3]])
        blue_channel = self.decrypt_grayscale([component_paths[4], component_paths[5]])
        red_pixels = red_channel.load()
        green_pixels = green_channel.load()
        blue_pixels = blue_channel.load()
        width, height = red_channel.size

        decrypted_image = Image.new("RGB", (width, height))
        decrypted_pixels = decrypted_image.load()

        for y in range(height):
            for x in range(width):
                decrypted_pixels[x, y] = (int(red_pixels[x, y]), int(green_pixels[x, y]), int(blue_pixels[x, y]))

        decrypted_image.save(f"{output_folder}/{output_name}.png")






