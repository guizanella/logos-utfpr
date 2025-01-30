import os
import random
import time
from PIL import Image
import re

# Mapeia os logos para as classes específicas baseado no nome do arquivo
def validate_manual_mapping(manual_mapping, logo_folder):
   
    # Obter todos os arquivos na pasta
    available_files = [f for f in os.listdir(logo_folder) if f.endswith(('png', 'jpg', 'jpeg'))]
    
    # Criar um dicionário baseando-se no nome das imagens dos logos sem número e extensão
    available_files_dict = {}
    for f in available_files:
        base_name = re.sub(r'\d+\.(png|jpg|jpeg)$', '', f)  # Remove números finais e extensão
        if base_name not in available_files_dict:
            available_files_dict[base_name] = []
        available_files_dict[base_name].append(os.path.join(logo_folder, f))
    
    # Validar e mapear os arquivos
    validated_mapping = {}
    for logo_id, class_name in manual_mapping.items():
        if class_name not in available_files_dict:
            raise FileNotFoundError(f"Nenhum arquivo encontrado para a classe '{class_name}' na pasta fornecida.")
        validated_mapping[logo_id] = [{"path": path, "tipo": class_name} for path in available_files_dict[class_name]]
    
    return validated_mapping

# Aplica os logos sobre os backgrounds
def apply_random_logos(background_folder, logo_folder, output_folder, classes, offset):

    # Certifique-se de que a pasta de saída existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Lista de imagens de background
    backgrounds = [os.path.join(background_folder, f) for f in os.listdir(background_folder) if f.endswith(('png', 'jpg', 'jpeg'))]

    if not backgrounds:
        print("Certifique-se de que há imagens de fundo nas pastas fornecidas.")
        return

    # Mapeia os logos para as classes
    logo_mapping = validate_manual_mapping(classes, logo_folder)
    
    # Embaralhar os logos para que sejam aplicados em ordem aleatória
    shuffled_logos = list(logo_mapping.items())
    random.shuffle(shuffled_logos)

    for i, background_path in enumerate(backgrounds):

        # Carregar um background
        background = Image.open(background_path).convert("RGBA")
        bg_width, bg_height = background.size

        # Divide o background em quatro quadrantes
        quadrants = [
            (0, 0, bg_width // 2, bg_height // 2), 
            (bg_width // 2, 0, bg_width, bg_height // 2),
            (0, bg_height // 2, bg_width // 2, bg_height),
            (bg_width // 2, bg_height // 2, bg_width, bg_height)
        ]

        # Criar arquivo .txt para a imagem
        txt_file_path = os.path.join(output_folder, f"result_{i + 1 + offset}.txt")
        with open(txt_file_path, "w") as txt_file:
            for quadrant in quadrants:
                # Selecionar uma classe de logo aleatória e, dentro dela, uma imagem aleatória
                logo_id, logo_info_list = random.choice(shuffled_logos)
                logo_info = random.choice(logo_info_list)  # Escolher uma das imagens da classe
                logo_path = logo_info["path"]
                logo = Image.open(logo_path).convert("RGBA")

                # Tamanho máximo do logo baseado no quadrante
                max_width = quadrant[2] - quadrant[0]
                max_height = quadrant[3] - quadrant[1]

                # Gerar um tamanho aleatório proporcional ao quadrante (40% a 80%)
                scale_factor = random.uniform(0.4, 0.8)
                aspect_ratio = logo.size[0] / logo.size[1]

                if aspect_ratio > 1:  # Logo é mais largo do que alto
                    logo_width = int(max_width * scale_factor)
                    logo_height = int(logo_width / aspect_ratio)
                else:  # Logo é mais alto do que largo
                    logo_height = int(max_height * scale_factor)
                    logo_width = int(logo_height * aspect_ratio)

                # Redimensionar o logo
                logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)

                # Calcular posição dentro do quadrante sem sobreposição
                x_start = random.randint(quadrant[0], quadrant[2] - logo.size[0])
                y_start = random.randint(quadrant[1], quadrant[3] - logo.size[1])
                x_end = x_start + logo.size[0]
                y_end = y_start + logo.size[1]

                # Colocar o logo sobre o background
                background.paste(logo, (x_start, y_start), logo)

                # Salvar informações no arquivo .txt
                txt_file.write(f"{logo_id}, {x_start}, {y_start}, {x_end}, {y_end}\n")

        # Salvar a imagem resultante
        background = background.convert("RGB")
        output_path = os.path.join(output_folder, f"result_{i + 1 + offset}.jpg")
        background.save(output_path, format="JPEG", quality=95)

# Caminhos para pastas de backgrounds
background_folders = {
    "corretos": "backgrounds_conjunto_editado/backgrounds_logo_correto",
    "errados": "backgrounds_conjunto_editado/backgrounds_logo_errado"
}

# Caminhos para pastas de logos
logo_folders = {
    "corretos": "conjunto_logos/corretos",
    "errados": "conjunto_logos/errados"
}

# Classes definidas
classes = {
    "corretos": {
        0: "correto",
    },
    "errados": {
        1: "baixa_resolucao",
        2: "cor_alterada",
        3: "distorcido",
        4: "fragmentado",
        5: "inclinado",
        6: "moldura",
        7: "outline",
        8: "proporcao",
        9: "rotacionado",
        10: "sombra",
        11: "tipologia"
    }
}

output_folder = "conjunto_treinamento"
offset = 0

for category in ["corretos", "errados"]:
    apply_random_logos(
        background_folders[category],
        logo_folders[category],
        output_folder,
        classes[category],
        offset
    )
    offset += len(os.listdir(background_folders[category]))
