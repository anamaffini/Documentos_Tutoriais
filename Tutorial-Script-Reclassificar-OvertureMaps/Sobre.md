# Sobre: `Script_Reclassificar_OvertureMaps.py`

**Autora:** Ana Luisa Maffini

**Ano:** 2026

**Contato:** analuisamaffini@gmail.com / analuisamaffini@ufrgs.br

## Para citar o Tutorial:

Maffini, A. L. (2026). Reclassificando Dados do Overture Maps: Comércio, Serviços e Outras Atividades com Python. Zenodo. https://doi.org/10.5281/zenodo.20452842

## Para citar o Script Python:

Maffini, A. L. (2026). Script para Reclassificar Dados do Overture Maps. Zenodo. https://doi.org/10.5281/zenodo.20452891


## Finalidade do script

Este script tem como objetivo **reclassificar dados de estabelecimentos extraídos do Overture Maps**, criando uma nova coluna chamada `categoria_atividade` em um arquivo GeoPackage (`.gpkg`).

A nova coluna classifica cada registro em três grupos principais:

- `comercio`: estabelecimentos associados a atividades comerciais;
- `servico`: estabelecimentos associados à prestação de serviços;
- `outros`: registros que não foram identificados pelas regras de comércio ou serviço.

O script foi pensado para ser utilizado em bases geoespaciais que contenham, pelo menos, as colunas `basic_category` e `taxonomy`, frequentemente presentes em dados de lugares, pontos de interesse ou estabelecimentos derivados do Overture Maps.

---

## O que o script faz

De forma geral, o código executa as seguintes etapas:

1. Importa as bibliotecas necessárias;
2. Define o caminho do arquivo GeoPackage de entrada;
3. Define o caminho do arquivo GeoPackage de saída;
4. Define o nome da camada a ser lida dentro do GeoPackage;
5. Lê os dados geoespaciais com `geopandas`;
6. Extrai informações textuais da coluna `taxonomy`;
7. Combina os textos das colunas `basic_category` e `taxonomy`;
8. Procura palavras-chave associadas a comércio e serviços;
9. Cria uma nova coluna chamada `categoria_atividade`;
10. Salva um novo GeoPackage com os dados reclassificados;
11. Exibe no terminal a contagem de registros por categoria.

---

## Bibliotecas necessárias

O script utiliza duas bibliotecas principais:

```python
import geopandas as gpd
import json
```

### `geopandas`

A biblioteca `geopandas` é utilizada para ler, manipular e salvar dados geoespaciais. Neste script, ela é responsável por:

- abrir o arquivo GeoPackage de entrada;
- acessar os atributos da camada;
- criar a nova coluna de classificação;
- salvar o resultado em um novo GeoPackage.

### `json`

A biblioteca `json` é uma biblioteca padrão do Python. Ela é usada para interpretar o conteúdo da coluna `taxonomy`, que pode estar armazenado em formato JSON.

Por ser uma biblioteca padrão, não é necessário instalá-la separadamente.

---

## Instalação das dependências

Antes de executar o script, é necessário ter o Python instalado e instalar o `geopandas`.

Uma forma recomendada de instalação é usar um ambiente virtual ou um ambiente Conda.

###  Instalação com `pip`

```bash
pip install geopandas
```

## Estrutura esperada dos dados de entrada

O arquivo de entrada deve ser um GeoPackage (`.gpkg`) contendo uma camada com dados geoespaciais de estabelecimentos.

A camada deve conter, preferencialmente, as seguintes colunas:

| Coluna | Descrição |
|---|---|
| `basic_category` | Categoria geral do estabelecimento |
| `taxonomy` | Classificação mais detalhada da atividade, geralmente em formato JSON |
| `geometry` | Geometria espacial do registro |

A coluna `geometry` é necessária para que o arquivo continue sendo um dado geoespacial válido.

---

## Parâmetros que o usuário precisa alterar

No início do script há três variáveis que devem ser ajustadas conforme o local dos arquivos no computador do usuário:

```python
entrada = r"c:\Users\Local_Entrada\Dados_Overture.gpkg"
saida = r"c:\Users\Local_Saida\Dados_Overture_reclassificado.gpkg"
camada = "Dados_Overture"
```

### `entrada`

Indica o caminho completo do arquivo GeoPackage original.

Exemplo:

```python
entrada = r"C:\Users\Ana\Documents\Dados_Overture.gpkg"
```

### `saida`

Indica o caminho completo onde será salvo o novo GeoPackage reclassificado.

Exemplo:

```python
saida = r"C:\Users\Ana\Documents\Dados_Overture_reclassificado.gpkg"
```

### `camada`

Indica o nome da camada dentro do GeoPackage.

Exemplo:

```python
camada = "Dados_Overture"
```

Se o nome da camada estiver incorreto, o script não conseguirá abrir o arquivo. É importante verificar o nome da camada no QGIS, no GeoPackage ou por meio de ferramentas Python.

---

## Explicação das principais partes do código

### 1. Leitura do GeoPackage

```python
gdf = gpd.read_file(entrada, layer=camada)
```

Esta linha lê a camada indicada na variável `camada`, dentro do GeoPackage definido em `entrada`.

O resultado é armazenado em um `GeoDataFrame`, chamado `gdf`.

Um `GeoDataFrame` é semelhante a uma tabela do Pandas, mas com suporte a geometrias espaciais.

---

### 2. Função `extrair_taxonomy_texto`

```python
def extrair_taxonomy_texto(valor):
```

Esta função transforma o conteúdo da coluna `taxonomy` em um texto simples, padronizado em letras minúsculas.

A coluna `taxonomy` pode conter uma estrutura JSON, por exemplo:

```json
{
  "primary": "bakery",
  "hierarchy": ["food_and_beverage_store", "store"]
}
```

A função procura dois elementos principais:

- `primary`: categoria principal da atividade;
- `hierarchy`: lista com categorias hierárquicas associadas ao registro.

Essas informações são reunidas em um único texto pesquisável.

Exemplo de resultado:

```text
bakery food_and_beverage_store store
```

Caso a função não consiga interpretar o valor como JSON, ela transforma o conteúdo original em texto e continua a execução. Isso evita que o script pare por causa de algum valor inesperado.

---

### 3. Função `classificar_estabelecimento`

```python
def classificar_estabelecimento(row):
```

Esta função é responsável por classificar cada estabelecimento.

Ela lê duas informações principais de cada linha:

```python
basic = str(row.get("basic_category", "")).lower()
taxonomy = extrair_taxonomy_texto(row.get("taxonomy", ""))
```

Em seguida, une os textos em uma única variável:

```python
texto = f"{basic} {taxonomy}"
```

Esse texto combinado é usado para procurar palavras-chave associadas a comércio ou serviço.

---

## Critérios de classificação

A classificação é feita por meio de listas de palavras-chave.

### Comércio

A lista `palavras_comercio` inclui termos associados a atividades comerciais, como:

- `store`;
- `shop`;
- `market`;
- `supermarket`;
- `grocery`;
- `bakery`;
- `pharmacy`;
- `clothing`;
- `electronics`;
- `furniture`;
- `hardware`;
- `convenience_store`;
- `pet_store`;
- `food_and_beverage_store`.

Quando qualquer uma dessas palavras aparece no texto combinado de `basic_category` e `taxonomy`, o registro é classificado como:

```text
comercio
```

### Serviços

A lista `palavras_servico` inclui termos associados à prestação de serviços, como:

- `service`;
- `salon`;
- `barber`;
- `laundry`;
- `office`;
- `attorney`;
- `accountant`;
- `real_estate`;
- `bank`;
- `insurance`;
- `clinic`;
- `hospital`;
- `automotive_repair`;
- `consulting`;
- `software`;
- `b2b`.

Quando qualquer uma dessas palavras aparece no texto combinado, o registro é classificado como:

```text
servico
```

### Outros

Caso nenhuma palavra-chave seja encontrada, o registro recebe a categoria:

```text
outros
```

---

## Ordem de prioridade da classificação

O script verifica primeiro as palavras associadas a comércio. Depois, verifica as palavras associadas a serviços.

Isso significa que, se um mesmo registro contiver uma palavra-chave de comércio e uma palavra-chave de serviço, ele será classificado como `comercio`.

Essa regra está definida nesta parte do código:

```python
if any(palavra in texto for palavra in palavras_comercio):
    return "comercio"

elif any(palavra in texto for palavra in palavras_servico):
    return "servico"

else:
    return "outros"
```

Caso seja necessário priorizar serviços em vez de comércio, basta inverter a ordem dessas verificações.

---

## Criação da nova coluna

A nova coluna é criada com a seguinte linha:

```python
gdf["categoria_atividade"] = gdf.apply(classificar_estabelecimento, axis=1)
```

Essa linha aplica a função `classificar_estabelecimento` a cada linha da tabela.

O resultado é armazenado na nova coluna `categoria_atividade`.

---

## Salvamento do arquivo final

O novo GeoPackage é salvo com:

```python
gdf.to_file(saida, layer=camada, driver="GPKG")
```

O arquivo final manterá as colunas originais e adicionará a coluna `categoria_atividade`.

O resultado será salvo no caminho definido na variável `saida`.

---

## Conferência dos resultados

Ao final, o script imprime no terminal a contagem de registros por categoria:

```python
print(gdf["categoria_atividade"].value_counts())
print("Arquivo salvo em:", saida)
```

O resultado será semelhante a:

```text
comercio    1200
servico      850
outros       430
Name: categoria_atividade, dtype: int64
Arquivo salvo em: C:\Users\Ana\Documents\Dados_Overture_reclassificado.gpkg
```

Essa etapa permite conferir rapidamente quantos registros foram classificados em cada grupo.

---

## Como executar o script no VS Code

1. Abra o VS Code;
2. Crie ou abra uma pasta de trabalho;
3. Coloque o arquivo `Script_Reclassificar_OvertureMaps.py` nessa pasta;
4. Abra o script no VS Code;
5. Altere as variáveis `entrada`, `saida` e `camada`;
6. Verifique se o ambiente Python está selecionado corretamente;
7. Instale as bibliotecas necessárias, se ainda não estiverem instaladas;
8. Execute o script pelo botão de execução do VS Code ou pelo terminal.

No terminal, o comando pode ser:

```bash
python Script_Reclassificar_OvertureMaps.py
```

---

## Como verificar o resultado no QGIS

Depois da execução:

1. Abra o QGIS;
2. Vá em **Camada > Adicionar Camada > Adicionar Camada Vetorial**;
3. Selecione o arquivo GeoPackage gerado;
4. Abra a tabela de atributos;
5. Verifique a nova coluna `categoria_atividade`;
6. Use simbologia categorizada para visualizar as classes `comercio`, `servico` e `outros`.

---

## Como adaptar o script

O usuário pode adaptar o script de acordo com seus objetivos de pesquisa ou com a estrutura da base de dados.

### Adicionar novas palavras-chave

Para incluir novas categorias comerciais, adicione termos à lista `palavras_comercio`.

Exemplo:

```python
"mall", "shopping_center", "wholesale"
```

Para incluir novas atividades de serviços, adicione termos à lista `palavras_servico`.

Exemplo:

```python
"education_service", "repair_service", "public_service"
```

### Alterar o nome da nova coluna

Se desejar usar outro nome para a coluna final, altere:

```python
gdf["categoria_atividade"]
```

Por exemplo:

```python
gdf["classe_uso"]
```

### Criar mais categorias

O script pode ser expandido para criar mais grupos, como:

- alimentação;
- saúde;
- educação;
- lazer;
- serviços financeiros;
- serviços automotivos;
- comércio varejista;
- comércio atacadista.

Para isso, é necessário criar novas listas de palavras-chave e novas condições dentro da função `classificar_estabelecimento`.

---

## Possíveis erros e soluções

### Erro: camada não encontrada

Verifique se o nome definido em `camada` corresponde exatamente ao nome da camada dentro do GeoPackage.

### Erro: arquivo não encontrado

Verifique se o caminho definido em `entrada` está correto.

No Windows, recomenda-se usar `r` antes do caminho:

```python
entrada = r"C:\Users\Ana\Documents\arquivo.gpkg"
```

### Erro relacionado ao `geopandas`

Caso o `geopandas` não esteja instalado, instale com:

```bash
pip install geopandas
```

ou:

```bash
conda install geopandas
```

### Resultado com muitos registros em `outros`

Isso pode ocorrer quando:

- os termos da coluna `taxonomy` não estão previstos nas listas de palavras-chave;
- a coluna `taxonomy` tem estrutura diferente da esperada;
- os dados possuem categorias muito específicas;
- os registros não correspondem a comércio nem serviço.

Nesse caso, recomenda-se abrir a tabela de atributos, observar os valores de `basic_category` e `taxonomy` dos registros classificados como `outros` e ampliar as listas de palavras-chave.

---

## Observações metodológicas

A classificação realizada pelo script é baseada em correspondência textual por palavras-chave. Portanto, ela é uma classificação operacional e reprodutível, mas não substitui uma revisão metodológica mais detalhada.

Recomenda-se revisar uma amostra dos registros classificados para verificar se as regras estão coerentes com o objetivo da análise.

Também é importante considerar que os dados do Overture Maps podem variar conforme a cobertura, a fonte original dos dados e a forma como as categorias foram preenchidas.

---

## Resultado esperado

Ao final da execução, o usuário terá um novo arquivo GeoPackage contendo:

- todos os dados originais;
- a geometria dos estabelecimentos;
- uma nova coluna chamada `categoria_atividade`;
- a classificação dos registros em `comercio`, `servico` ou `outros`.

