import os
import requests

os.makedirs("data", exist_ok=True)

files = {
    "dicionario_variaveis_2024.xlsx": "https://cetic.br/media/microdados/842/tic_kids_online_brasil_2024_dicionario_de_variaveis_v1.1.xlsx",
    "microdados_2024.csv": "https://cetic.br/media/microdados/844/tic_kids_online_brasil_2024_base_de_microdados_v1.2.csv",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

for name, url in files.items():
    dest = os.path.join("data", name)
    if os.path.exists(dest):
        print(f"{name} já existe ({os.path.getsize(dest)} bytes).")
        continue
    print(f"Baixando {name} de {url}...")
    try:
        r = requests.get(url, headers=headers, stream=True, timeout=60)
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
        print(f"{name} baixado com sucesso! ({os.path.getsize(dest)} bytes)")
    except Exception as e:
        print(f"Erro ao baixar {name}: {e}")
