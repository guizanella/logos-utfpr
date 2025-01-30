from PIL import Image, ImageEnhance, ImageOps
import os

# Função para alterar o brilho
def apply_brightness(img, brightness_factor):
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(brightness_factor)

# Função para aplicar zoom
def apply_zoom(img, zoom_factor):
    width, height = img.size
    crop_width, crop_height = int(width / zoom_factor), int(height / zoom_factor)
    left = (width - crop_width) // 2
    top = (height - crop_height) // 2
    right = (width + crop_width) // 2
    bottom = (height + crop_height) // 2
    return img.crop((left, top, right, bottom)).resize((width, height))

# Função para aplicar escala de cinza
def apply_grayscale(img):
    return ImageOps.grayscale(img)

# Função para aplicar efeito negativo
def apply_negative(img):
    return ImageOps.invert(img)

# Função para inverter valores RGB
def swap_rgb(img):
    pixels = img.load()
    width, height = img.size
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            pixels[x, y] = (g, b, r)
    return img

# Função para dividir e inverter horizontalmente
def invert_horizontal(img):
    width, height = img.size
    top_half = img.crop((0, 0, width, height // 2))
    bottom_half = img.crop((0, height // 2, width, height))
    img_horizontal_inverted = Image.new('RGB', (width, height))
    img_horizontal_inverted.paste(bottom_half, (0, 0))
    img_horizontal_inverted.paste(top_half, (0, height // 2))
    return img_horizontal_inverted

# Função para dividir e inverter verticalmente
def invert_vertical(img):
    width, height = img.size
    left_half = img.crop((0, 0, width // 2, height))
    right_half = img.crop((width // 2, 0, width, height))
    img_vertical_inverted = Image.new('RGB', (width, height))
    img_vertical_inverted.paste(right_half, (0, 0))
    img_vertical_inverted.paste(left_half, (width // 2, 0))
    return img_vertical_inverted

# Função para dividir em quadrantes e reorganizar
def swap_quadrants(img):
    width, height = img.size
    upper_left = img.crop((0, 0, width // 2, height // 2))
    upper_right = img.crop((width // 2, 0, width, height // 2))
    lower_left = img.crop((0, height // 2, width // 2, height))
    lower_right = img.crop((width // 2, height // 2, width, height))
    
    img_quadrant_swap = Image.new('RGB', (width, height))
    img_quadrant_swap.paste(lower_right, (0, 0))
    img_quadrant_swap.paste(lower_left, (width // 2, 0))
    img_quadrant_swap.paste(upper_right, (0, height // 2))
    img_quadrant_swap.paste(upper_left, (width // 2, height // 2))
    return img_quadrant_swap

# Função para espelhar horizontalmente e verticalmente
def apply_mirror(img):
    return img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)


# Função principal para editar as imagens
def edit_images(input_folder, output_folder, brightness_factor=2, zoom_factor=1.5):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            name, ext = os.path.splitext(filename)
            image_path = os.path.join(input_folder, filename)
            img = Image.open(image_path)
            img = img.convert("RGB")
        
            # Salva as imagens
            img.save(os.path.join(output_folder, filename))
            apply_brightness(img, brightness_factor).save(os.path.join(output_folder, f"{name}_bright.jpg"))
            apply_zoom(img, zoom_factor).save(os.path.join(output_folder, f"{name}_zoom.jpg"))
            apply_grayscale(img).save(os.path.join(output_folder, f"{name}_grayscale.jpg"))
            apply_negative(img).save(os.path.join(output_folder, f"{name}_negative.jpg"))
            invert_horizontal(img).save(os.path.join(output_folder, f"{name}_inverted_horizontal.jpg"))
            invert_vertical(img).save(os.path.join(output_folder, f"{name}_inverted_vertical.jpg"))
            swap_quadrants(img).save(os.path.join(output_folder, f"{name}_quadrant_swap.jpg"))
            apply_mirror(img).save(os.path.join(output_folder, f"{name}_mirror.jpg"))
            swap_rgb(img).save(os.path.join(output_folder, f"{name}_swapped_rgb.jpg"))

    print("Edição de imagens concluída.")


input_folder = 'conjunto_entrada'
output_folder = 'conjunto_saida'
edit_images(input_folder, output_folder)
