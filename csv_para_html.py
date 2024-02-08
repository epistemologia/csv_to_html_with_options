import glob
import csv
# from analisa_arquivo_csv import analisa
# from filtros_e_excecoes import trata_excecoes


# Use glob.glob to find CSV files in the current directory
def identifica_arquivos_csv() -> list:
    lista_arquivos_csv = glob.glob("*.csv")
    # lista_arquivos_csv.remove("excecoes.csv")
    return lista_arquivos_csv


# Use glob.glob to find "antes.html" files in the current directory
def encontra_antes_html() -> bool:
    lista_arquivos_csv = glob.glob("antes.html")
    return len(lista_arquivos_csv) > 0

# Use glob.glob to find "depois.html" files in the current directory


def encontra_depois_html() -> bool:
    lista_arquivos_csv = glob.glob("depois.html")
    return len(lista_arquivos_csv) > 0

# Use glob.glob to find "css.css" files in the current directory


def encontra_css_css() -> bool:
    lista_arquivos_csv = glob.glob("css.css")
    return len(lista_arquivos_csv) > 0


def copia_antes_html(nome_de_arquivo: str):
    with open(nome_de_arquivo, "a", encoding="utf-8") as saida:
        with open("antes.html", "r", encoding="utf-8") as entrada:
            for conteudo in entrada:
                saida.write(conteudo)
    return


def copia_depois_html(nome_de_arquivo: str):
    with open(nome_de_arquivo, "a", encoding="utf-8") as saida:
        with open("depois.html", "r", encoding="utf-8") as entrada:
            for conteudo in entrada:
                saida.write(conteudo)
    return


def copia_css_css(nome_de_arquivo: str):
    with open(nome_de_arquivo, "a", encoding="utf-8") as saida:
        with open("css.css", "r", encoding="utf-8") as entrada:
            for conteudo in entrada:
                saida.write(conteudo)
    return


def escolhe_arquivo_entrada(x: list) -> str:
    if len(x) == 1:
        return x[0]
    return ("A determinar")


def le_databook(nome_de_arquivo: str) -> tuple:
    lista = []
    cabecalhos = []
    contador = -1
    with open(nome_de_arquivo, 'r', encoding='cp1252') as f:
        reader = csv.reader(f, delimiter=',')
        for registro in reader:
            contador += 1
            if contador == 0:
                cabecalhos = registro
                cabecalhos.insert(0, "#")
                continue
            lista.append(registro)
        return cabecalhos, lista


def cabecalho_tabela(cab: list) -> str:
    linha = "<thead>\n<tr class='cabecalho'>"
    for campo in cab:
        linha += "<th>" + campo + "</th>"
    linha += "</tr>\n</thead>\n"
    return linha


def abre_tabela() -> str:
    return "<table class='tabela_01'>\n"


def fecha_tabela() -> str:
    return "</table>\n"


def fecha_html(arquivo_saida: str):
    if encontra_depois_html():
        copia_depois_html(arquivo_saida)
    with open(arquivo_saida, "a", encoding='utf-8') as h:
        h.write("</body>\n</html>\n")
    return


def escreve_linha_tabela(contador: int, reg: list) -> str:
    resultado = '<tr><th>' + str(contador) + "</th>"
    for campo in reg:
        resultado += "<td>" + campo + "</td>"
    resultado += "</tr>\n"
    return resultado


def cria_arq_saida(nome_saida: str, cabecalho: list, registros: list):
    inicia_html(nome_saida)
    if encontra_antes_html():
        copia_antes_html(nome_saida)
    contador = 0
    with open(nome_saida, 'a', encoding='utf-8') as g:
        g.write(abre_tabela())
        g.write(cabecalho_tabela(cabecalho))
        for registro in registros:
            contador += 1
            g.write(escreve_linha_tabela(contador, registro))
        g.write(fecha_tabela())
    fecha_html(nome_saida)
    return


def inicia_html(nome_arquivo_saida: str):
    with open(nome_arquivo_saida, 'w', encoding='utf-8') as g:
        g.write("""<!doctype html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<style>
body {
  -webkit-print-color-adjust: exact !important;
  padding:2em;
  background-color: ivory;
}
* { 
	color-adjust: exact;
	-webkit-print-color-adjust: exact;
	print-color-adjust: exact;
   font-family: monospace;
}
@media print {
  table tr {
    break-inside: avoid;
  }
  thead {
    display: table-header-group;
  }
}
table.tabela_01 {
  border:1px solid black;
  background-color: white;
}
table.tabela_01 th, table.tabela_01 td {
  padding:0.8em;
}
table.tabela_01 tr.cabecalho {
  background-color: lightblue;
}
tr:nth-child(2n) { background-color: lightgray; border: 0; }
tr:nth-child(2n+1) { background-color: silver; border: 0; }
th { border: 2px solid black; }
td { border: 1px solid black; }
/*
	Contador de linhas
*/
table tbody {
	counter-reset: cnt;
}
table tbody tr th.cnt::before {
	counter-increment: cnt;
	content: counter(cnt)".";
}
tbody td.cnt::before {
	counter-increment: cnt;
	content: counter(cnt)".";
}\n""")
    encerra_css(nome_arquivo_saida)
    return


def encerra_css(arquivo_saida: str):
    if encontra_css_css():
        copia_css_css(arquivo_saida)
    with open(arquivo_saida, 'a', encoding='utf-8') as g:
        g.write("""</style>
</head>
<body>
""")
    return


def main() -> list:
    # lista de nomes de arquivo (com extensão ".csv")
    csv_arquivos = identifica_arquivos_csv()
    arq_ent = escolhe_arquivo_entrada(csv_arquivos)
    #
    # A primeira linha é tratada como fonte de cabeçalhos (títulos, nomes dos campos)
    # A segunda linha em diante são tratadas como informação efetiva
    cabecalhos, lista = le_databook(arq_ent)

    print("\n\n"+str(len(lista)) +
          " registros de foram encontrados no arquivo CSV e serão convertidos para uma tabela HTML com cabeçalho.")

    print("Se houver um arquivo 'css.css' neste diretório, ele será integrado ao arquivo 'saida.html' final;")
    print("se houver um arquivo 'antes.html' neste diretório, ele será integrado ao arquivo 'saida.html' antes da tabela;")
    print("se houver um arquivo 'depois.html' neste diretório, ele será integrado ao arquivo 'saida.html' depois da tabela.\n\n\n")
    x = input("Tecle <enter> para criar o arquivo 'saida.html': ")
    cria_arq_saida("saida.html", cabecalhos, lista)
    x = input("Tecle <enter> para encerrar. ")

    return


if __name__ == '__main__':
    main()
