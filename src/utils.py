import cv2
import os
import glob
import numpy as np

# --- CONFIGURAÇÃO ---
# Usando caminhos relativos para evitar erros de digitação e acentos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(BASE_DIR, 'dataset', 'raw')
OUTPUT_DIR = os.path.join(BASE_DIR, 'dataset', 'processed')
TARGET_SIZE = (640, 640)

os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_images():
    # Usando set() para evitar que o Windows conte .jpg e .JPG como arquivos diferentes
    image_files = set()
    extensions = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.PNG', '*.JPEG']
    
    for ext in extensions:
        files = glob.glob(os.path.join(INPUT_DIR, ext))
        for f in files:
            image_files.add(os.path.abspath(f))

    image_files = list(image_files)

    if not image_files:
        print(f"❌ Nenhuma imagem encontrada em: {INPUT_DIR}")
        return

    print(f"🔄 Encontradas {len(image_files)} imagens únicas para processar...")

    count = 0
    for img_path in image_files:
        try:
            # SOLUÇÃO PARA O ERRO DO "SÉRGIO": 
            # Em vez de cv2.imread, lemos o arquivo como um array de bytes e decodificamos
            img_array = np.fromfile(img_path, np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            if img is None:
                print(f"⚠️ Erro ao decodificar: {img_path}")
                continue

            # Redimensionar
            resized_img = cv2.resize(img, TARGET_SIZE, interpolation=cv2.INTER_AREA)

            # Salvar com novo nome
            new_name = f"epi_{count:03d}.jpg"
            save_path = os.path.join(OUTPUT_DIR, new_name)

            # SOLUÇÃO PARA SALVAR EM PASTAS COM ACENTO:
            # Codificamos a imagem e salvamos o buffer no arquivo
            result, enc_img = cv2.imencode('.jpg', resized_img)
            if result:
                with open(save_path, mode='wb') as f:
                    enc_img.tofile(f)
                count += 1
            
        except Exception as e:
            print(f"❌ Erro em {img_path}: {e}")

    print("-" * 30)
    print(f"🎉 SUCESSO! {count} imagens processadas em '{OUTPUT_DIR}'.")

if __name__ == "__main__":
    process_images()