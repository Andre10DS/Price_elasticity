# Price Elasticity

## Este projeto visa criar uma ferramenta para facilitar a avaliação do impacto na demanda após a alteração nos preços de cada produto.
O projeto consistir em criar uma ferramenta para a empresa Consultoria Varejo S.A. que facilite a análise da mudança e o impacto da mudança no preço em determinados produtos de cada loja de varejo. Tal ferramenta poderá ser comercializada junto aos varejistas que ppoderão disponibilizar aos seus times de precificação com o intuito de embasar, facilitar e melhorar as análises de determinação do preço.

Para cumprir o objetivo será desenvolvido um modelo baseado em regressão para determinar a elasticidade do preço de cada produto utilizando a base de dados disponilizada pelos varejistas.

A elasticidade-preço é um conceito da Economia que verifica a relação entre a variação no preço e demanda, mensurando o quando a alteração no preço influencia na demanda por determinado produto. Esse conceito pode ser utilizado para auxiliar o processo de markup otimizando o tempo e maximizando o faturamento.

# 1. Problema de negócio.
A empresa Consultoria Varejo S.A. precisa de uma ferramenta que auxilie no processo de markup facilitando as análises e possibilitando a visualização de oportunidades de maximização do faturamento.


# 2. Premissas de negócio.

1. Deve ser criado uma ferramenta para auxiliar nas análises de determinação do markup e qeu possibilite aos times de price a verificação de oportunidades de ganho no faturamento.
2. O resultado deverá ser entregue em dashboard no streamlit.
3. Em um primeiro momento deverá ser entregue uma análise somente da categoria de "laptop, computer".
4. A primeira varejista a ser analisada é a Bestbuy.com;
5. Para a análise será adotado um desconto de 10% na categoria em avaliação.

# 3. Objetivo.

1. Entregar um dashboard no streamlit em que o usuário possa escolher entre desconto ou aumento além do percentual a ser aplicado. Após a escolha e o input dos dados a ferramenta irá retonar a elasticidade de cada produto, bem como o impacto no faturamento. 

# 4. Planejamento da solução.
## 4.1 Produto final.
  - Modelo de mensuração da elastiidade de cada produto e o impacto no faturamento.
  - Construção de um dashboard no streamlit.
    
## 4.2 Ferramentas.
  1. Jupyter notebook;
  2. VSCode;
  3. Streamlit;
  4. Git e Github;
  5. Python 3.9.17;
  6. Algoritmo de regressão linear.
  
## 4.3 Processo.
### 4.3.1. Estratégia da solução.

**Step 01. Descrição dos dados:**

  - Realizar a descrição das colunas.
  - Maperar as hipoteses.
  - Ajustar o nome das colunas.
  - Checar os tipos de dados e verificar a necessidade de alteração.
  - Checar os NA e realizar e o replace caso necessário.
  - Relizar a descrição estatisticas dos dados númericos e avaliar distorções.

**Step 02. Criação de Features:**

  - Realizar a construção de novos features ou o ajuste dos dados daquelas existentes.

**Step 03. Filtragem de dados:**

  - Filtragem de dados que possuem restrições de negócio. (Nesta base de dados não foi verificado a necessidade de realizar tal ação)

**Step 04. Analise exploratória dos dados:**

  - Realizar a análise univariada.
  - Realizar a análise bivariada.

**Step 05. Preparação dos dados:**

  - Realizar a separação dos dados de treino e validação (Não foi utilizada neste projeto).
  - Padronizar os dados númericos com a distribuição normal (Não foi utilizada neste projeto).
  - Realizar a reescalar dos dados (Não foi utilizada neste projeto).
  - Realizar o encooding dos dados categóricos (Não foi utilizada neste projeto).
  - Aplicar transormações de natureza (Não foi utilizada neste projeto).
  - Realizar as transformações nos dados de validação (Não foi utilizada neste projeto).

**Step 06. Seleção de Features:**

  - Nesta etapa foi utilizado somente as features de price, Number_weeK e Date_imp_d	

**Step 07. Modelo de Machine Learning e Hyperparameter Fine Tunning:(Não foi realizado neste projeto)**

**Step 08. Conversão da performance do modelo em resultados de negócio:**

  - Desdobrar os resultados do modelo em performance de negócio.
  - Traduzir a performance em retorno financeiro para a empresa. 

**Step 10. Deploy do modelo em produção:**

  - Criar um scripty que possa ser executado no streamlit.
  - Exportar o scripty para o Git.
  - Efetuar o deploy do scripty no streamlit.

# 5. Aplicação do modelo de Machine Learning

Para o desenvolvimento do projeto foi utilizado o modelo de regressão linear da biblioteca statsmodels. A biblioteca possui funções que possibilita a verificação e utilização do coeficiente angula para calcular a elasticidade do preço.

# 6. Performance do modelo de Machine Learning escolhido

Nesta etapa atráves da utilização do modelo de regressão linear foi possivel verificar os valores de elasticidade, coeficiente angular e p-valor que possbilita 


<img src="https://github.com/Andre10DS/Price_elasticity/blob/main/img/Performance.png?raw=true" alt="Produtos" title="Elasticidade do preço-demanda da categoria Laptop, computer" align="center" height="400" class="center"/>

Podemos verificar na tabela acima que os produtos que apresentaram maiores elasticidade foram o Dell - Inspiron 15.6 Laptop - Intel Core i5 - 8GB Memory (-34.12), 12 MacBook (-32.58) e o Details About Apple Macbook Air 13.3 Laptop (-11.61). 


# 7. Resultados para o negócio

Conforme premissa adotada para a analise será realizada um desconto de 10% no preço dos produtos da categoria "laptop, computer". Segue abaixo a tabela de impacto com a relação do faturamento atual,  o novo faturamento, a variação nominal do faturamento e a variação percentual do faturamento:


<img src="https://github.com/Andre10DS/Price_elasticity/blob/main/img/Impacto.png?raw=true" alt="Produtos" title="Impacto no faturamento com o desconto de 10% no preço dos pordutos da categoria Laptop, computer" align="center" height="400" class="center"/>


Com base nos resultados obtidos na tabela acima pode ser verificado se o desconto de 10% fosse aplicado a todos o produtos da categoria "laptop, computer" teríamos tanto produtos com aumento quanto com redução de receita. O impacto seria um crescimento de US$ 18.714,91. Porém, se fosse adotado o desconto somente nos produtos que apresentassem aumento no faturamento teríamos um incremento de US$ 42.744,77.

### Acesse o dashboard - [Dashstreamlit](https://priceelasticity-es9sfqf4ub8qbyavgytw43.streamlit.app/)

# 8. Conclusão

Ao verificar os resultados do projeto podemos constatar que o objetivo foi concluído conforme planejado.

Ao utilizar as ferramentas os varejistas poderão acelerar o processo de precificação, melhorar a tomada de descição com a utilização de dados e verificar a possibilidade de maximização do faturamento em determinadas categorias e linhas de produtos.


# 9. Próximos passos

- Criar um descritivo com detalhamento do impacto de forma automática.

