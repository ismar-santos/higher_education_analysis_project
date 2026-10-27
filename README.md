# Análise de Evasão no Ensino Superior

Segundo o [Instituto Semesp](https://www.semesp.org.br/mapa/edicao-16/brasil/), a taxa de evasão nos cursos presenciais de ensino superior público no Brasil foi em média 21% nos anos de 2018 à 2024. Estas desistências desencadeiam uma série de problemas tanto para os estudantes quanto para a sociedade, como, por exemplo, menor retorno dos investimentos públicos em educação e aumento do custo por estudante formado.

## Objetivo do projeto

O objetivo é responder a pergunta:
<p align='center'>Quais características dos cursos estão associadas a maiores taxas de evasão, e é possível antecipar quais cursos terão evasão alta no ano seguinte?</p>

## Dataset

O conjunto de dados utilizado é disponibilizado de forma pública, proveniente da Universidade Federal do Paraná (UFPR). O dataset contém informações sobre cursos de ensino superior da mesma universidade, cada linha possui informações de um curso em um determinado ano. Como não existe id, consideramos que, em conjunto, as colunas curso, campus, grau e turno definem cada curso. Idealmente, um ano deve possuir no máximo uma instância de cada curso. Na fonte, os dados disponibilizados pela UFPR são separados por ano, portanto é necessário corrigir, transformar e concatenar os CSVs para um carregamento de dados bem sucedido. Foi escolhido o período de 2018 à 2025.

**Fonte**: [Quantitativo de Alunos de Graduação](https://ufpr.br/transparencia/quantitativo-de-alunos-de-graduacao/)