import requests
import zipfile
import io
import os
from datetime import datetime

url_pendentes ="https://api-csvr.cloud.cnj.jus.br/download_csv?tribunal=TJRS&indicador=ind2&oj=&grau=&municipio=&procedimento=&ambiente=csv_p"
url_novos ="https://api-csvr.cloud.cnj.jus.br/download_csv?tribunal=TJRS&indicador=ind1&oj=&grau=&municipio=&procedimento=&ambiente=csv_p"
url_baixados ="https://api-csvr.cloud.cnj.jus.br/download_csv?tribunal=TJRS&indicador=ind3&oj=&grau=&municipio=&procedimento=&ambiente=csv_p"

destino = "dados_cnj"
#destino = r"endereço da pasta"
def extrair_csv(resposta, pasta_destino):
    os.makedirs(pasta_destino,exist_ok=True)
    arquivo_zip = io.BytesIO(resposta.content)

    with zipfile.ZipFile(arquivo_zip) as zip_ref:
        nome_csv = zip_ref.namelist()[0]

        caminho_completo_csv = os.path.join(pasta_destino, nome_csv)

        if os.path.exists(caminho_completo_csv):
            agora = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_base = nome_csv.replace(".csv","")
            nome_backup = f"{nome_base}_OLD_{agora}.csv"

            caminho_completo_backup = os.path.join(pasta_destino, nome_backup)
            os.rename(caminho_completo_csv,caminho_completo_backup)
            print(f"[Backup] Arquivo antigo renomeado para: {nome_backup}")

        zip_ref.extract(nome_csv, pasta_destino)
        print(f"[Sucesso] Arquivo {nome_csv}salvo na pasta'{pasta_destino}'")


print("Iniciando comunicação com o servidor ...")

resposta_pendentes = requests.get(url_pendentes)
resposta_novos = requests.get(url_novos)
resposta_baixados = requests.get(url_baixados)

print("Downloads concluídos, começando a extração")

extrair_csv(resposta_pendentes, destino)
extrair_csv(resposta_baixados, destino)
extrair_csv(resposta_novos, destino)

print ("Processo finalizado")