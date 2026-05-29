# Importações de Bibliotecas Necessárias

import geopandas as gpd
import json


# Informações que o Usuário precisa alterar!

# Caminho do arquivo de entrada
entrada = r"c:\Users\Local_Entrada\Dados_Overture.gpkg"

# Caminho do arquivo de saída
saida = r"c:\Users\Local_Saida\Dados_Overture_reclassificado.gpkg"

# Nome da camada dentro do GeoPackage
camada = "Dados_Overture"


# A partir daqui o usuário não precisa alterar mais nada.

# Ler o GeoPackage
gdf = gpd.read_file(entrada, layer=camada)

def extrair_taxonomy_texto(valor):
    """
    Transforma a coluna taxonomy em texto pesquisável.
    A taxonomy do arquivo está em formato JSON.
    """
    if valor is None:
        return ""

    try:
        tax = json.loads(valor) if isinstance(valor, str) else valor

        textos = []

        if isinstance(tax, dict):
            if "primary" in tax:
                textos.append(str(tax["primary"]))

            if "hierarchy" in tax and isinstance(tax["hierarchy"], list):
                textos.extend([str(x) for x in tax["hierarchy"]])

        return " ".join(textos).lower()

    except Exception:
        return str(valor).lower()


def classificar_estabelecimento(row):
    basic = str(row.get("basic_category", "")).lower()
    taxonomy = extrair_taxonomy_texto(row.get("taxonomy", ""))

    texto = f"{basic} {taxonomy}"

    # Palavras associadas a comércio
    palavras_comercio = [
        "store", "shop", "market", "supermarket", "grocery",
        "bakery", "butcher", "pharmacy", "drug_store",
        "clothing", "fashion", "apparel", "shoe", "jewelry",
        "electronics", "computer_store", "furniture",
        "hardware", "home_goods", "garden", "gift",
        "book", "music", "video", "sporting_goods",
        "department_store", "convenience_store",
        "auto_parts", "vehicle_parts", "pet_store",
        "beauty_supply", "food_and_beverage_store",
        "flowers", "candy", "dessert", "ice_cream"
    ]

    # Palavras associadas a serviços
    palavras_servico = [
        "service", "salon", "beauty_salon", "barber",
        "spa", "nail", "tattoo", "laundry", "laundromat",
        "office", "professional", "attorney", "law_firm",
        "accountant", "engineering", "architectural",
        "real_estate", "financial", "bank", "insurance",
        "clinic", "dental", "health", "hospital",
        "psychologist", "physical_therapy", "veterinarian",
        "automotive_repair", "car_wash", "auto_detailing",
        "construction", "design", "printing",
        "marketing", "advertising", "photography",
        "travel_service", "shipping", "delivery",
        "transportation", "it_service", "computer_repair",
        "software", "consulting", "b2b"
    ]

    if any(palavra in texto for palavra in palavras_comercio):
        return "comercio"

    elif any(palavra in texto for palavra in palavras_servico):
        return "servico"

    else:
        return "outros"


# Criar nova coluna
gdf["categoria_atividade"] = gdf.apply(classificar_estabelecimento, axis=1)

# Salvar novo GeoPackage
gdf.to_file(saida, layer=camada, driver="GPKG")

# Conferir resultado
print(gdf["categoria_atividade"].value_counts())
print("Arquivo salvo em:", saida)