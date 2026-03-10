import os
import re
from collections import defaultdict
from langchain_community.document_loaders import PyPDFLoader

PDF_PATH = "vias_escalada_de_montesclaros.pdf"
OUTPUT_DIR = "rag_docs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

loader = PyPDFLoader(PDF_PATH)
pages = loader.load()

vias = []

via = None
grau = None
setor = None
local = None

for page in pages:
    lines = page.page_content.split("\n")

    for line in lines:
        line = line.strip()

        if line.startswith("Via:"):
            via = line.replace("Via:", "").strip()

        elif line.startswith("Grau:"):
            grau = line.replace("Grau:", "").strip()

            if grau == "":
                grau = "Não graduada"

            if "?" in grau:
                grau = grau.replace("?", "").strip()
                grau = f"{grau} (estimado)"

        elif line.startswith("Setor:"):
            setor = line.replace("Setor:", "").strip()

        elif line.startswith("Local:"):
            local = line.replace("Local:", "").strip()

        if via and grau and setor and local:
            vias.append({
                "via": via,
                "grau": grau,
                "setor": setor,
                "local": local
            })

            via = None
            grau = None
            setor = None
            local = None


setores = defaultdict(list)

for v in vias:
    key = (v["local"], v["setor"])
    setores[key].append(v)


for (local, setor), lista_vias in setores.items():

    filename = f"{local}_{setor}".lower()
    filename = filename.replace(" ", "_")
    filename = filename.replace("º", "")
    filename += ".txt"

    path = os.path.join(OUTPUT_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:

        f.write(f"Local: {local}\n")
        f.write(f"Setor: {setor}\n")
        f.write(f"Total de vias: {len(lista_vias)}\n\n")
        f.write("Vias:\n\n")

        for v in lista_vias:
            f.write(f"Via: {v['via']}\n")
            f.write(f"Grau: {v['grau']}\n\n")

print("Documentos criados em:", OUTPUT_DIR)