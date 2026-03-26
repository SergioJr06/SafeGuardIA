import qrcode
import sys
import os

def gerar_qr_code(url):
    # Lógica de caminho para salvar na raiz do projeto
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    OUTPUT_PATH = os.path.join(BASE_DIR, "dashboard_qr.png")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(OUTPUT_PATH)
    print(f"✅ QR Code gerado e salvo em: {OUTPUT_PATH}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Uso: python generate_qr.py SUA_URL_DO_NGROK")
    else:
        url_input = sys.argv[1]
        gerar_qr_code(url_input)