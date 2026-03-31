from roboflow import Roboflow

# Substitua pela sua chave
rf = Roboflow(api_key="dQpWX3D6YGOh3XSO5ogq")

# Exemplo de como baixar um dataset do Universe
# Vá na página do dataset no Universe e pegue o ID (ex: "workspace/projeto/versao")
project = rf.workspace("alexandro-romeira").project("epi-det")
dataset = project.version(1).download("yolov8")

print("✅ Dataset baixado com sucesso!")