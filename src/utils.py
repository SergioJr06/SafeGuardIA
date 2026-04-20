import cv2
import os
import glob
import numpy as np

# ==========================================================
# Pré-processamento de Dataset — SafeGuard IA
# Redimensiona imagens brutas para 640x640 e as salva
# em /dataset/processed com nomes padronizados.
# ==========================================================

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR  = os.path.join(BASE_DIR, "dataset", "raw")
OUTPUT_DIR = os.path.join(BASE_DIR, "dataset", "processed")
TARGET_SIZE = (640, 640)

os.makedirs(OUTPUT_DIR, exist_ok=True)


def process_images():
    # Coleta arquivos de todas as extensões suportadas.
    # Usa abspath + set() para evitar duplicatas em sistemas
    # case-insensitive (Windows) onde .jpg e .JPG seriam contados duas vezes.
    extensions  = ["*.jpg", "*.jpeg", "*.png", "*.JPG", "*.PNG", "*.JPEG"]
    image_files = set()

    for ext in extensions:
        for f in glob.glob(os.path.join(INPUT_DIR, ext)):
            image_files.add(os.path.abspath(f))

    image_files = list(image_files)

    if not image_files:
        print(f"Nenhuma imagem encontrada em: {INPUT_DIR}")
        return

    print(f"Imagens encontradas: {len(image_files)}")
    print(f"Destino           : {OUTPUT_DIR}")
    print("-" * 48)

    processadas = 0
    erros       = 0

    for img_path in image_files:
        try:
            # np.fromfile + imdecode evita erros em caminhos com
            # caracteres especiais ou acentuados (comum no Windows).
            img_array = np.fromfile(img_path, np.uint8)
            img       = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            if img is None:
                print(f"  [AVISO] Nao foi possivel decodificar: {img_path}")
                erros += 1
                continue

            resized = cv2.resize(img, TARGET_SIZE, interpolation=cv2.INTER_AREA)

            new_name  = f"epi_{processadas:04d}.jpg"
            save_path = os.path.join(OUTPUT_DIR, new_name)

            # imencode + tofile para salvar em caminhos com acento (Windows)
            ok, enc_img = cv2.imencode(".jpg", resized, [cv2.IMWRITE_JPEG_QUALITY, 95])
            if ok:
                enc_img.tofile(save_path)
                processadas += 1
            else:
                print(f"  [AVISO] Falha ao codificar: {img_path}")
                erros += 1

        except Exception as e:
            print(f"  [ERRO] {img_path}: {e}")
            erros += 1

    print("-" * 48)
    print(f"Concluido: {processadas} imagens processadas, {erros} erro(s).")
    print(f"Saida     : {OUTPUT_DIR}")


if __name__ == "__main__":
    process_images()