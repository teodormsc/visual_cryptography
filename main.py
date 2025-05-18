from encryptor import Encryptor
from decryptor import Decryptor
from halftone_converter import HalftoneConverter

converter = HalftoneConverter()
encryptor = Encryptor()
decryptor = Decryptor()

print("Dithering Grayscale ...")
converter.grayscale_bayer_dithering("input/books.png", 4, output_name="books_bayer")
converter.grayscale_floyd_steinberg_dithering("input/books.png", output_name="books_floyd_steinberg")

print("Encrypting Grayscale ...")
encryptor.encrypt_grayscale("output/books_bayer.png", output_one_name="books_component_one", output_two_name="books_component_two")

print("Decrypting Grayscale ...")
decryptor.decrypt_grayscale(["output/books_component_one.png", "output/books_component_two.png"], output_name="books_decrypted")

#-----------------------------------------------------------------------------------------------------------------------

print("Dithering Color ...")
converter.color_bayer_dithering("input/mountain.png", 4, red_channel_name="mountain_bayer_red",
                                green_channel_name="mountain_bayer_green", blue_channel_name="mountain_bayer_blue")

print("Encrypting Color ...")
encryptor.encrypt_color(["output/mountain_bayer_red.png", "output/mountain_bayer_green.png", "output/mountain_bayer_blue.png"],
                        red_one_name="mountain_red_one", red_two_name="mountain_red_two", green_one_name="mountain_green_one",
                        green_two_name="mountain_green_two", blue_one_name="mountain_blue_one", blue_two_name="mountain_blue_two")

print("Decrypting Color ...")
component_paths = ["output/mountain_red_one.png", "output/mountain_red_two.png", "output/mountain_green_one.png",
                   "output/mountain_green_two.png", "output/mountain_blue_one.png", "output/mountain_blue_two.png"]
decryptor.decrypt_color(component_paths, output_name="mountain_decrypted")