# COVID-19 World Survey Data API


Este script tem como objetivo facilitar a comunicação com a API [COVID-19 World Survey Data](https://covidmap.umd.edu/api.html) para extrair os relatórios das pesquisas para os estados e regiões brasileiras. Para saber mais sobre os indicadores, acesse: https://covidmap.umd.edu/api.html

Para exectuar esse script, é necessário que você siga os passos abaixo:

## Instalando python3 e dependências via Anaconda

1. Baixe e instale o miniconda3 em seu computador: https://docs.conda.io/en/latest/miniconda.html
2. Selecione a versão de acordo com o seu sistema operacional. Não é necessário baixar a versão com python 3.7!
3. Após seguir todos os passos da instalação, procure pelo terminal do anaconda em seu computador digitando "Anaconda".
4. Crie uma nova variável ambiente com python 3.7:
```bash
conda create -n py37 python=3.7 
```
5. Ative sua nova variável ambiente com python 3.7:
```bash
conda activate py37
```
_Usuários de MacOS_
```bash
source activate py37
```
6. Após ativar sua nova variável, ela deve ficar da seguinte maneira antes do caminho no bash `(py37)`.
7. Instale as dependências executando a seguinte linha de comando:
```bash
conda install pandas numpy openpyxl requests
```
8. Navegue até o diretório do repositório e siga o tutorial abaixo para extrair as informações desejadas.

*Usuários do sistema operacional MacOS Big Sur poderão enfrentar problemas durante a instalação do ambiente python.*

## Extraindo o relatório

A extração do relatório com as informações listadas anteriormente pode ser realizada das seguintes maneiras:

### Todos os Estados (Brasil)
Para extrair as informações de todos estados basta executar o script da seguinte maneira:
```bash
python report.py
```

### Região do Brasil
Caso você queira extrair as informações de uma determinada região, basta informar o nome dessa região ao parâmetro `-r`:
```bash
python report.py -r sul
```
O relatório resultante será da combinação de todos os estados presentes na região. Haverá uma coluna `region` indicado a qual estado pertence o resultado da pesquisa.

### Filtro por Estado único
```bash
python report.py -e sigla_estado
```
Exemplo com os dados do Paraná:
```bash
python report.py -e pr
```

### Filtro por Estados combinados
Para extrair as informações de mais de um estado, basta informar as siglas dos estados desejados separados por vígula `,`:
```bash
python report.py -e pr,rs,sc
```
O relatório resultante será da combinação de todos os estados informados no parâmetro. Haverá uma coluna `region` indicado a qual estado pertence o resultado da pesquisa.

### Utilizando outros indicadores
Para extrair as informações de outro indicador que não seja covid, basta informar o nome da seguinte maneira:
```bash
python report.py -i mask
```
O relatório conterá as colunas relacionadas com o indicador `mask`. Para saber mais sobre os indicadores, acesse: https://covidmap.umd.edu/api.html


### Parâmetros adicionais
- Nome do arquivo de saída (sem extensão): `-o`
- Formato do arquivo de saída (excel ou csv): `-f`
```bash
python report.py -f xlsx
```

Para quaisquer dúvidas, sinta-se livre para me contatar via e-mail ou Github.