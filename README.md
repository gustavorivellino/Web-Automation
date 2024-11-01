Projeto de Comparação de Preços com Web Scraping
Este projeto realiza web scraping em Google Shopping e Buscapé para buscar e comparar preços de produtos. Ele utiliza uma planilha de entrada contendo informações sobre os produtos e filtra as ofertas conforme uma faixa de preços e termos banidos. O resultado é consolidado em uma tabela e exportado para um arquivo Excel.

Objetivo
Automatizar a busca e comparação de preços em plataformas de e-commerce, facilitando a consulta de ofertas e filtrando produtos indesejados, além de definir um intervalo de preço adequado para cada item pesquisado.

Funcionalidades
Busca automatizada: O script acessa Google Shopping e Buscapé para buscar produtos.
Filtros de produtos: Remove produtos indesejados com termos banidos e verifica se todos os termos do produto estão presentes no nome.
Faixa de preço: Filtra os produtos dentro do preço mínimo e máximo especificado.
Consolidação de dados: Gera uma planilha Excel consolidada com as ofertas encontradas.

Estrutura do Projeto
Arquivo de entrada: buscas.xlsx - Planilha contendo o nome do produto, termos banidos, preço mínimo e máximo.
Script principal: Código em Python que utiliza Selenium para web scraping e Pandas para manipulação de dados.
Arquivo de saída: tabela_ofertas.xlsx - Planilha com os resultados das buscas.
