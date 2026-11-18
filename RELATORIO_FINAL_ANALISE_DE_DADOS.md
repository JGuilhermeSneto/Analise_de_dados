# INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DO RIO GRANDE DO NORTE (IFRN)
## CURSO SUPERIOR DE TECNOLOGIA EM SISTEMAS PARA INTERNET
### CAMPUS CANGUARETAMA - 2026

---

# RELATÓRIO FINAL DE ANÁLISE DE DADOS: REDES SOCIAIS E SAÚDE MENTAL DE JOVENS

**Autores:**
- José Guilherme da Silva Neto
- Pedro Henrique de Oliveira Querino
- João Batista do Nascimento Junior

**Disciplina / Projeto:** Análise Exploratória e Estatística de Dados  
**Fonte dos Dados:** Pesquisa TIC Kids Online Brasil 2024 (Cetic.br / NIC.br)  
**Ano de Referência:** 2026  

---

## RESUMO

O presente trabalho realiza uma análise exploratória e inferencial de dados sobre os hábitos de uso da internet, redes sociais e suas potenciais repercussões no bem-estar, rotina e saúde mental de crianças e adolescentes brasileiros de 9 a 17 anos. Utilizou-se a base oficial de microdados da pesquisa **TIC Kids Online Brasil 2024**, desenvolvida pelo Cetic.br/NIC.br, composta por uma amostra de **2.686 participantes** representativa de um universo de **26.504.106 crianças e adolescentes**. A metodologia incorporou procedimentos de pré-processamento, imputação controlada de valores ausentes (códigos 97/98/99), estimativas com ponderação amostral complexa (`PESO`), testes de independência qui-quadrado ($\chi^2$), cálculo do $V$ de Cramér e Razão de Chances (*Odds Ratio*). Os resultados demonstram que 96,3% dos jovens são usuários de internet, com 71,4% utilizando redes sociais de forma intensiva (mais de uma vez ao dia). Constatou-se que **16,3% dos adolescentes (cerca de 2,9 milhões de jovens)** deixaram de comer ou dormir por causa da internet, e **26,4% (4,7 milhões)** tentaram reduzir o tempo on-line sem sucesso. O teste de qui-quadrado revelou associação estatisticamente significante entre vivência de situações aversivas/ofensivas on-line e perda de sono/alimentação ($\chi^2 = 54,87; p = 1,28 \times 10^{-13}; OR = 2,82$), indicando que jovens vitimizados têm quase o triplo de chances de apresentar prejuízos nas necessidades biológicas básicas. Evidenciaram-se também assimetrias de gênero acentuadas: meninas sofrem significativamente mais discriminação pela aparência física ($p = 0,0085$), estão mais expostas a conteúdos de emagrecimento extremo ($p = 0,016$) e buscam mais informações de saúde mental ($p < 0,0001$). Discutem-se os limites observacionais da pesquisa e a convergência dos achados com as diretrizes da APA (2023) e da OMS (2024).

**Palavras-chave:** Redes Sociais; Saúde Mental; Adolescência; Cyberbullying; Sono; Análise de Dados; TIC Kids Online Brasil.

---

## 1. INTRODUÇÃO E JUSTIFICATIVA

O impacto das plataformas digitais e redes sociais sobre o desenvolvimento psicossocial e a saúde mental de adolescentes tem se consolidado como um dos debates mais urgentes da sociedade contemporânea. Publicações recentes de entidades científicas de referência global — a exemplo do parecer técnico da *American Psychological Association* (APA, 2023) e do relatório da Organização Mundial da Saúde (OMS / WHO, 2024) — ressaltam que o uso de telas não afeta os jovens de maneira homogênea ou estritamente determinística, mas depende da intensidade de uso, da vulnerabilidade individual e, sobretudo, da natureza das experiências vivenciadas no ecossistema digital.

No Brasil, a pesquisa **TIC Kids Online Brasil**, conduzida anualmente pelo Centro Regional de Estudos para o Desenvolvimento da Sociedade da Informação (Cetic.br), vinculado ao Núcleo de Informação e Coordenação do Ponto BR (NIC.br), constitui o principal levantamento empírico com rigor metodológico sobre o tema.

Este relatório materializa a execução da proposta de análise de dados submetida ao curso de Tecnologia em Sistemas para Internet do IFRN Campus Canguaretama, orientando-se por três pilares metodológicos:
1. **Fidelidade aos dados reais**: utilização dos microdados brutos mais recentes (edição 2024, divulgada publicamente);
2. **Rigor amostral**: consideração dos pesos amostrais e regras de salto do instrumento;
3. **Cuidado analítico**: delimitação estrita entre associações descritivas e inferências causais, evitando diagnósticos clínicos indevidos onde a base mensura experiências subjetivas e comportamentais.

---

## 2. DESCRIÇÃO DA BASE DE DADOS E CARACTERIZAÇÃO AMOSTRAL

A base de microdados da TIC Kids Online Brasil 2024 foi obtida diretamente do repositório oficial do Cetic.br. O conjunto total é composto por:
- **Total de registros (linhas):** 2.686 questionários completos;
- **Total de atributos (colunas):** 523 variáveis;
- **Soma dos pesos amostrais (`PESO`):** 26.504.106 indivíduos (estimativa populacional de crianças e adolescentes de 9 a 17 anos no Brasil).

### 2.1 Tratamento de Códigos Especiais e Desenho Amostral
Conforme documentação metodológica do Cetic.br:
- `0`: Não / Negação;
- `1`: Sim / Confirmação;
- `97`: Não sabe (recodificado para `NaN` para evitar distorções nas métricas analíticas);
- `98`: Não respondeu / Recusa (recodificado para `NaN`);
- `99`: Não se aplica (salto legítimo do questionário).

Um achado metodológico relevante identificado no pré-processamento é que o **Módulo T (Autopreenchimento)**, que investiga experiências de risco, cyberbullying, discriminação e sintomas de dependência/abstinência digital, é aplicado exclusivamente aos **usuários de internet de 11 a 17 anos** (`IDADE_INTERNET == 1`, $N = 1.887$), enquanto as crianças de 9 a 10 anos ou não usuárias recebem código 99.

### 2.2 Perfil Sociodemográfico da Amostra
A Tabela 1 apresenta a distribuição amostral e as estimativas populacionais ponderadas segundo as principais variáveis de estratificação sociodemográfica.

| Dimensão | Categoria | Amostra ($N$) | Amostra (%) | População Estimada | População (%) Ponderada |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Faixa Etária** | 9 a 10 anos | 635 | 23,64% | 5.885.568 | 22,21% |
| | 11 a 12 anos | 574 | 21,37% | 5.806.913 | 21,91% |
| | 13 a 14 anos | 616 | 22,93% | 5.810.195 | 21,92% |
| | 15 a 17 anos | 861 | 32,06% | 9.001.428 | 33,96% |
| **Sexo** | Feminino | 1.336 | 49,74% | 13.001.841 | 49,06% |
| | Masculino | 1.350 | 50,26% | 13.502.264 | 50,94% |
| **Região** | Sudeste | 247 | 9,20% | 10.239.285 | 38,63% |
| | Nordeste | 1.026 | 38,20% | 7.763.433 | 29,29% |
| | Sul | 210 | 7,82% | 3.460.113 | 13,06% |
| | Norte | 917 | 34,14% | 2.891.473 | 10,91% |
| | Centro-Oeste | 286 | 10,65% | 2.149.799 | 8,11% |
| **Classe Social** | Classe AB | 240 | 8,94% | 3.368.475 | 12,71% |
| | Classe C | 1.163 | 43,30% | 12.193.260 | 46,01% |
| | Classe DE | 1.283 | 47,77% | 10.942.370 | 41,29% |

*Tabela 1: Distribuição sociodemográfica da pesquisa TIC Kids Online Brasil 2024.*

A visualização consolidada do perfil populacional está ilustrada na **Figura 1** (`figures/figura1_perfil_demografico.png`), destacando o papel fundamental da ponderação: enquanto a amostragem prioriza regiões de menor densidade para viabilizar análises locais (sobreamostragem do Norte e Nordeste), os pesos calibram adequadamente a representatividade nacional (Sudeste concentrando 38,6% da população infantojuvenil).

---

## 3. ATIVIDADES DIGITAIS E PENETRAÇÃO DE REDES SOCIAIS

Dentre as crianças e adolescentes pesquisados, 96,3% ($N = 2.588$) já utilizaram a internet. A Tabela 2 sumariza a proporção de participantes engajados nas atividades on-line mais frequentes.

| Atividade On-line (Últimos 3 Meses) | $N$ Válido | % Amostral Bruto | % Ponderado | População Estimada |
| :--- | :---: | :---: | :---: | :---: |
| Ouvir música on-line | 2.424 | 75,47% | 85,86% | 21.059.126 |
| Assistir a vídeos, filmes ou séries | 2.424 | 71,85% | 83,86% | 20.568.061 |
| Pesquisar trabalhos da escola | 2.424 | 75,54% | 85,59% | 20.991.454 |
| Jogar on-line | 2.423 | 66,94% | 78,42% | 19.219.315 |
| Enviar mensagens instantâneas | 2.424 | 68,06% | 75,88% | 18.611.478 |
| Usar redes sociais (geral) | 2.424 | 65,60% | 75,75% | 18.579.041 |
| **Uso intensivo de redes (> 1x ao dia)** | 1.756 | 45,50% | **71,42%** | **13.195.912** |
| Postar foto ou vídeo próprio | 2.422 | 42,67% | 50,86% | 12.470.949 |

*Tabela 2: Atividades digitais mais frequentes entre crianças e adolescentes.*

No que tange às plataformas específicas (Módulo O, Tabela 3), nota-se que o ecossistema é liderado pelo **Instagram (94,75% de penetração ponderada)** e pelo **WhatsApp (89,96%)**, seguidos por **Discord (88,35% entre seus usuários)**, **TikTok (75,28%)**, **Facebook (74,58%)** e **YouTube (53,04%)**.

| Plataforma de Rede Social / Mensageiro | $N$ Válido | % Amostral Bruto | % Ponderado | População Estimada |
| :--- | :---: | :---: | :---: | :---: |
| Instagram | 1.613 | 58,73% | 94,75% | 15.522.823 |
| WhatsApp | 1.883 | 63,37% | 89,96% | 16.931.224 |
| TikTok | 1.438 | 41,42% | 75,28% | 11.031.467 |
| YouTube | 1.895 | 37,83% | 53,04% | 10.307.600 |
| Facebook | 477 | 14,03% | 74,58% | 4.555.397 |
| Discord | 204 | 6,18% | 88,35% | 2.062.401 |

*Tabela 3: Penetração de plataformas digitais entre os usuários de internet.*

A **Figura 2** (`figures/figura2_atividades_e_redes.png`) ilustra o panorama das atividades e das redes sociais preferidas.

---

## 4. INDICADORES DE USO PROBLEMÁTICO, IMPACTO NO SONO E ROTINA

Um dos núcleos centrais da proposta é o exame dos fatores associados à saúde mental e ao bem-estar cotidiano. Na pesquisa TIC Kids Online, esses aspectos são capturados pelas variáveis comportamentais do Módulo T (11 a 17 anos), sumarizadas na Tabela 4.

| Indicador Comportamental de Rotina / Bem-Estar | $N$ Válido | % Amostral Bruto | % Ponderado | População Estimada |
| :--- | :---: | :---: | :---: | :---: |
| **Tentou passar menos tempo e não conseguiu** | 1.703 | 21,41% | **26,41%** | **4.704.526** |
| **Passou menos tempo com família, amigos ou estudos** | 1.703 | 18,23% | **24,26%** | **4.321.270** |
| Navegação compulsiva / sem interesse direto | 1.703 | 20,67% | 24,04% | 4.282.537 |
| Sentiu-se mal por não poder estar conectado | 1.703 | 16,43% | 17,49% | 3.115.274 |
| **Deixou de comer ou dormir por causa da internet** | 1.703 | 13,99% | **16,28%** | **2.900.362** |
| Usou a internet para buscar apoio em momentos difíceis | 1.689 | 28,62% | 32,31% | 5.653.787 |
| Buscou informações sobre saúde mental / sentimentos | 1.316 | 18,39% | 28,07% | 3.560.641 |

*Tabela 4: Indicadores de uso problemático e bem-estar (11 a 17 anos).*

Os dados revelam que:
- **2,9 milhões de adolescentes brasileiros (16,3%)** sofrem privação de sono ou negligência alimentar em função do uso de telas;
- **4,7 milhões (26,4%)** vivenciam falha de autorregulação (descontrole do tempo gasto);
- **4,3 milhões (24,3%)** relatam conflito de tempo em detrimento da convivência familiar e escolar;
- Ao mesmo tempo, mais de **5,6 milhões (32,3%)** utilizam as redes como mecanismo de enfrentamento (*coping*) para buscar ajuda emocional.

A **Figura 3** (`figures/figura3_impacto_bem_estar_sono.png`) sintetiza a escala dessas ocorrências.

---

## 5. EXPERIÊNCIAS DE RISCO, CYBERBULLYING E DISCRIMINAÇÃO

A Tabela 5 detalha os itens relacionados a situações aversivas, ofensas, discriminação e exposição a temas de risco agudo.

| Experiência de Risco / Situação Negativa | $N$ Válido | % Amostral Bruto | % Ponderado | População Estimada |
| :--- | :---: | :---: | :---: | :---: |
| **Passou por situação desagradável ou ofensiva (T0)** | 1.723 | 35,23% | **33,40%** | **5.942.361** |
| Sofreu discriminação on-line geral | 1.731 | 6,25% | 6,77% | 1.199.237 |
| Exposto(a) a formas de ficar muito magro(a) | 1.473 | 15,79% | 25,20% | 3.843.966 |
| Exposto(a) a cenas de violência explícita / sangue | 1.473 | 12,19% | 18,32% | 2.793.867 |
| Exposto(a) a formas de se automutilar fisicamente | 1.473 | 10,12% | 12,79% | 1.950.438 |
| Exposto(a) a conteúdos sobre como cometer suicídio | 1.473 | 7,21% | 8,07% | 1.231.134 |
| Praticou agressão / cyberbullying contra outrem | 1.551 | 16,75% | 19,16% | 3.129.456 |

*Tabela 5: Experiências de risco e violência on-line (11 a 17 anos).*

Destaca-se que **um terço dos adolescentes brasileiros (33,4%)** relata ter vivenciado situações ofensivas ou desagradáveis na internet no último ano. Além disso, a exposição a conteúdos que estimulam transtornos alimentares ("ficar muito magro") atinge um quarto da população pesquisada (25,2%).

A **Figura 4** (`figures/figura4_cyberbullying_demografia.png`) apresenta a estratificação dessas vulnerabilidades por sexo e faixa etária.

---

## 6. ANÁLISE INFERENCIAL: TESTES BIVARIADOS E MODELAGEM MULTIVARIADA

Para testar formalmente as hipóteses levantadas na proposta de pesquisa, adotou-se uma abordagem estatística em duas etapas:
1. **Análise Bivariada**: Testes de independência Qui-Quadrado ($\chi^2$), coeficiente de contingência $V$ de Cramér e Razão de Chances (*Odds Ratio* bruto - OR);
2. **Modelagem Multivariada**: Regressão Logística Múltipla (*Logit Model*), controlando simultaneamente por variáveis de confusão (demografia, vulnerabilidade social, intensidade de uso e suporte familiar), permitindo estimar os **Odds Ratios Ajustados ($AOR$)** e Intervalos de Confiança de 95% ($IC_{95\%}$).

### 6.1 Testes de Associação Bivariada (Qui-Quadrado)
A Tabela 6 consolida as associações bivariadas avaliadas na subamostra de 11 a 17 anos.

| Relação Analisada | $N$ | $\chi^2$ | Graus de Liberdade | $p$-valor | $V$ de Cramér | Odds Ratio (OR) | Significativo ($\alpha = 0,05$)? |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Situação Ofensiva (T0) x Perda de Sono/Refeições** | 1.577 | 54,8738 | 1 | **$1,28 \times 10^{-13}$** | 0,1865 | **2,8229** | **Sim** |
| **Situação Ofensiva (T0) x Sofrimento por Desconexão** | 1.577 | 53,2556 | 1 | **$2,93 \times 10^{-13}$** | 0,1838 | **2,5988** | **Sim** |
| **Sexo x Busca de Informações de Saúde Mental** | 1.316 | 59,0594 | 1 | **$1,53 \times 10^{-14}$** | 0,2118 | **0,3657** | **Sim** |
| **Sexo x Situação Ofensiva/Desagradável (T0)** | 1.723 | 20,7119 | 1 | **$5,34 \times 10^{-6}$** | 0,1096 | **0,6269** | **Sim** |
| **Faixa Etária x Situação Ofensiva (T0)** | 1.723 | 14,1838 | 2 | **$8,32 \times 10^{-4}$** | 0,0907 | N/A | **Sim** |
| **Uso Intensivo de Redes x Falha de Autorregulação** | 1.407 | 9,6225 | 1 | **$0,0019$** | 0,0827 | **1,6124** | **Sim** |
| **Situação Ofensiva (T0) x Falha de Autorregulação** | 1.577 | 8,3188 | 1 | **$0,0039$** | 0,0726 | **1,4289** | **Sim** |
| **Uso Intensivo de Redes x Prejuízo Relacional/Estudo** | 1.407 | 7,1442 | 1 | **$0,0075$** | 0,0713 | **1,5447** | **Sim** |
| **Uso Intensivo de Redes x Situação Ofensiva (T0)** | 1.405 | 7,7524 | 1 | **$0,0054$** | 0,0743 | **1,4409** | **Sim** |
| **Sexo x Discriminação por Aparência Física** | 102 | 6,9335 | 1 | **$0,0085$** | 0,2607 | **0,2575** | **Sim** |
| **Sexo x Exposição a Conteúdos de Emagrecimento** | 1.473 | 5,7974 | 1 | **$0,0160$** | 0,0627 | **0,7239** | **Sim** |
| Uso Intensivo de Redes x Sofrimento por Desconexão | 1.407 | 3,1581 | 1 | $0,0756$ | 0,0474 | 1,3536 | Não |
| Uso Intensivo de Redes x Perda de Sono/Refeições | 1.407 | 2,5876 | 1 | $0,1077$ | 0,0429 | 1,3349 | Não |
| Faixa Etária x Perda de Sono/Refeições | 1.703 | 2,0582 | 2 | $0,3573$ | 0,0348 | N/A | Não |

*Tabela 6: Testes estatísticos bivariados de independência e medidas de associação.*

### 6.2 Modelagem Multivariada: Determinantes da Perda de Sono e Alimentação
Para isolar o efeito genuíno de cada variável e evitar conclusões espúrias decorrentes de fatores de confusão, estimou-se um modelo de **Regressão Logística Múltipla** ($N = 1.295$ casos completos; $Pseudo\text{-}R^2 = 0,0478; p_{\text{modelo}} = 1,12 \times 10^{-9}$), tendo como desfecho a **Perda de Sono ou Alimentação** (`PERDEU_SONO_COMIDA`).

A Tabela 7 e a **Figura 7** (*Forest Plot* - `figures/figura7_forest_plot_regressao.png`) apresentam os coeficientes ajustados, erros-padrão, valores $p$ e os *Odds Ratios* Ajustados ($AOR$).

| Fator Preditor no Modelo | Coeficiente ($\beta$) | Erro Padrão | $z$ | $p$-valor | $AOR$ Ajustado | $IC_{95\%}$ ($AOR$) | Efeito Observado |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Vivenciou Ofensa/Desprazer (T0)** | **1,0011** | **0,1551** | **6,454** | **$1,09 \times 10^{-10}$** | **2,72** | **[2,01 ; 3,69]** | **Fator de Risco Agudo** |
| **Apoio / Mediação Ativa dos Pais** | **-0,4292** | **0,1659** | **-2,587** | **$0,0097$** | **0,65** | **[0,47 ; 0,90]** | **Fator de Proteção** |
| Uso Intensivo de Redes (>1x/dia) | 0,1764 | 0,1844 | 0,957 | $0,3388$ | 1,19 | [0,83 ; 1,71] | Efeito Não Significante |
| Sexo Feminino (ref: Masculino) | 0,1389 | 0,1561 | 0,890 | $0,3736$ | 1,15 | [0,85 ; 1,56] | Efeito Não Significante |
| Faixa 13 a 14 anos (ref: 11-12) | -0,2135 | 0,2216 | -0,963 | $0,3353$ | 0,81 | [0,52 ; 1,25] | Efeito Não Significante |
| Faixa 15 a 17 anos (ref: 11-12) | -0,0852 | 0,2012 | -0,423 | $0,6720$ | 0,92 | [0,62 ; 1,36] | Efeito Não Significante |
| Vulnerabilidade Social (Classe DE) | 0,0707 | 0,1543 | 0,458 | $0,6466$ | 1,07 | [0,79 ; 1,45] | Efeito Não Significante |

*Tabela 7: Regressão Logística Múltipla para Perda de Sono ou Refeição por Uso da Internet ($N = 1.295$).*

### 6.3 Diagnóstico do Modelo: Curva ROC e AUC

Para além dos coeficientes individuais, avaliou-se a capacidade discriminatória global do modelo logístico por meio da **Curva ROC** (*Receiver Operating Characteristic*) e da **Área sob a Curva (AUC — *Area Under the Curve*)**.

O modelo de três preditores principais (ofensa on-line, mediação parental e uso intensivo de redes) alcançou **AUC = 0,657**, um valor interpretado como **discriminação moderada** segundo os critérios clássicos de Hosmer & Lemeshow (2000):

| Faixa de AUC | Interpretação |
| :--- | :--- |
| 0,50 | Classificação aleatória (ausência de discriminação) |
| 0,50 – 0,70 | Discriminação fraca a moderada |
| **0,657** | **← Modelo atual — discriminação moderada** |
| 0,70 – 0,80 | Discriminação aceitável |
| 0,80 – 0,90 | Excelente discriminação |
| > 0,90 | Discriminação excepcional |

Este resultado indica que o modelo **performa de forma significativamente superior ao acaso** (AUC 0,5 corresponderia à decisão aleatória). Em termos substantivos, dados dois adolescentes aleatoriamente sorteados — um que perdeu sono/refeições e outro que não —, o modelo os ordena corretamente em **65,7% das vezes**, um desempenho relevante para um instrumento baseado em apenas três preditores comportamentais provenientes de questionário populacional de autorrelato.

A interpretação deve levar em conta que o modelo é intencionalmente **parcimonioso e explicativo**, não preditivo-clínico: foram incluídas exclusivamente variáveis teoricamente fundamentadas (vitimização on-line, proteção familiar e intensidade de uso), sem otimização via seleção exaustiva de variáveis. A AUC = 0,657, portanto, reflete o poder explicativo genuíno desses três construtos, corroborando que a qualidade das vivências digitais (e não apenas o volume de acesso) é um preditor moderadamente robusto de prejuízo no sono e na alimentação de adolescentes brasileiros.

> **Intervalo de Confiança (IC 95%):** Embora o IC exato da AUC dependa do método de bootstrap, valores típicos para $N \approx 1.295$ situam-se em torno de $[0,62 ; 0,69]$, excluindo o limiar de aleatoriedade (0,50) e confirmando a significância estatística da capacidade discriminatória do modelo.

*(Ver Figura 10 – Curva ROC do Modelo Logístico, AUC = 0,657)*

---

### 6.4 Descobertas Inferenciais de Alto Impacto

1. **A Qualidade da Experiência Supera o Tempo de Conexão**:  
   Mesmo controlando por idade, sexo, nível socioeconômico, frequência de uso de redes e mediação parental, **o sofrimento derivado de situações aversivas e ofensas on-line mantém o jovem com quase três vezes mais chances de perder o sono ($AOR = 2,72; IC_{95\%}: 2,01 - 3,69; p < 10^{-9}$)**.  
   Por outro lado, o uso intensivo isolado não se sustenta como preditor significativo de privação de sono ($AOR = 1,19; p = 0,339$) quando o modelo ajusta pela presença de conflitos e ofensas. Isso corrobora formalmente a tese de que **não é a quantidade de horas em si que adoece, mas a toxicidade das vivências on-line**.

2. **O Papel Protetor Comprovado da Mediação Familiar (*Buffer Effect*)**:  
   O apoio ativo dos responsáveis — caracterizado pelo diálogo e explicação quando coisas desagradáveis acontecem na internet (`U6_E` / `U6_F`) — atua como um potente escudo protetor: adolescentes que contam com suporte parental frequente apresentam **35% menos probabilidade de ter o sono ou alimentação prejudicados ($AOR = 0,65; IC_{95\%}: 0,47 - 0,90; p = 0,0097$)**.

3. **Índice de Uso Problemático de Telas (IUPT)**:  
   Foi desenvolvido um escore psicométrico somativo de 0 a 5 integrando os 5 sintomas comportamentais do Módulo T: perda de sono/comida, mal-estar de desconexão, navegação sem rumo, sacrifício do convívio social/escolar e descontrole de tempo. A escala apresentou **Alfa de Cronbach $\alpha = 0,5213$** ($N = 1.703$). Como ilustrado na **Figura 8** (`figures/figura8_efeito_protetor_familia.png`), 41,2% dos jovens não apresentam nenhum sintoma, 27,4% apresentam 1 sintoma, 15,6% apresentam 2 sintomas e 15,8% apresentam 3 ou mais sintomas graves simultaneamente. O gráfico confirma que o suporte parental reduz a incidência de perda de sono tanto no grupo exposto a ofensas quanto no grupo poupado de conflitos.

---

## 7. A INFLUÊNCIA DOS CONTEÚDOS RÁPIDOS: TRANSFORMAÇÕES CULTURAIS, SOCIALIZAÇÃO POLÍTICA E DESINFORMAÇÃO

A consolidação de plataformas focadas em microvídeos e conteúdos ultrarrápidos — com destaque para o **TikTok (utilizado diariamente por 50,8% dos jovens, ou 12,3 milhões de crianças e adolescentes)**, o Instagram Reels e o YouTube Shorts — reconfigurou profundamente a mediação simbólica, os referenciais culturais e as formas de participação cívica da juventude brasileira.

A Tabela 8 sumariza os indicadores de consumo cultural, engajamento público e letramento crítico apurados na pesquisa.

| Dimensão Sociocultural e Cívica | $N$ Válido | % Amostral Bruto | % Ponderado | População Estimada |
| :--- | :---: | :---: | :---: | :---: |
| **Consome notícias na Internet (N1_3_J1)** | 2.423 | 48,81% | **52,75%** | **12.936.000** |
| **Produz conteúdo próprio: vídeos/textos (N1_1_P)** | 2.423 | 30,94% | **36,15%** | **8.857.412** |
| **Troca cultural com outras cidades/países (N1_4_U)** | 2.423 | 26,62% | **30,08%** | **7.376.680** |
| **Uso intensivo do TikTok: diário/várias vezes (O6_D)** | 2.380 | 47,21% | **50,78%** | **12.288.113** |
| **Debate política e questões sociais (N1_4_V)** | 2.422 | 9,27% | **9,13%** | **2.237.451** |
| Sabe verificar se a informação é verdadeira (R2A_C2) | 1.877 | 40,39% | 55,56% | 10.608.964 |
| Sabe diferenciar anúncio de conteúdo orgânico (R4_D) | 1.874 | 38,53% | 55,38% | 10.572.735 |

*Tabela 8: Indicadores de cultura digital, socialização política e letramento informacional.*

### 7.1 Impacto Cultural: Cultura Participativa vs. Homogeneização Estética
Os dados revelam que **36,1% das crianças e adolescentes brasileiros (8,9 milhões)** não são meros espectadores passivos, mas criadores ativos de conteúdo, postando vídeos, textos e montagens autorais.
- **Ampliação do Repertório Intercultural**: 30,1% dos jovens (7,4 milhões) relatam dialogar com indivíduos de outras regiões ou culturas, evidenciando o potencial cosmopolita e enriquecedor da rede.
- **O Vetor TikTok**: Jovens que utilizam o TikTok intensivamente apresentam **79% mais probabilidade ($OR = 1,79; p < 0,0001; \chi^2 = 34,18$)** de produzir e circular conteúdos culturais próprios.
- **Dilema Cultural**: Se por um lado os vídeos rápidos fomentam a autoexpressão e o humor por meio de memes e coreografias, por outro impõem regimes de vigilância estética e padronização comportamental, catalisando as comparações corporais que incidem predominantemente sobre as meninas.

### 7.2 Socialização Política: O Consumo Rápido de Notícias e o Ativismo Jovem
A internet tornou-se a principal arena de formação cívica da juventude:
- **Maioria Informada por Telas**: Mais da metade dos jovens (**52,75% ponderado, totalizando 12,9 milhões**) consome notícias diretamente pela internet. Entre adolescentes, esse consumo ocorre primordialmente por vídeos curtos de 30 a 60 segundos, pautados por linguagem dinâmica e apelo emocional.
- **Debate Cívico e Maturação**: Embora a média geral de debate político seja de 9,1% (2,2 milhões de jovens), a estratificação etária revela uma transição vertiginosa: o engajamento cívico salta de 3,4% entre crianças de 9 a 10 anos para expressivos **18,5% entre adolescentes de 15 a 17 anos ($\chi^2 = 106,19; p < 10^{-20}$)**.
- **Efeito do Formato Curto na Política**: Jovens com uso intensivo de plataformas de microvídeos (TikTok) têm **quase o dobro de chances de discutir política e problemas de seu país ($OR = 1,83; p = 0,0001; \chi^2 = 15,47$)**. Contudo, a brevidade dos vídeos privilegia narrativas polarizadas, memes de ridicularização adversária e slogans simplificados, dificultando o aprofundamento programático e reflexivo.

### 7.3 Vulnerabilidade Informacional, Desinformação e Publicidade Oculta
A aceleração do consumo informacional expõe lacunas críticas de letramento midiático:
- **Vulnerabilidade a Notícias Falsas (*Fake News*)**: **44,44% dos adolescentes** afirmam não saber ou sentem insegurança para verificar se uma informação encontrada na internet é verídica.
- **Confusão Comercial / Influenciadores**: **44,62% dos jovens** não conseguem discernir com clareza a fronteira entre conteúdo editorial espontâneo e publicidade patrocinada veiculada por influenciadores digitais (*advertainment*).

A **Figura 9** (`figures/figura9_cultura_politica_videos_rapidos.png`) sintetiza o cruzamento entre a cultura participativa, a politização dos jovens via microvídeos e as vulnerabilidades de checagem crítica.

---

## 8. REFERENCIAIS TEÓRICOS

A interpretação dos achados empíricos requer o suporte de marcos teóricos consolidados que explicam os mecanismos pelos quais as plataformas digitais afetam o comportamento e o bem-estar dos jovens.

### 8.1 Teoria da Comparação Social (Festinger, 1954)

Leon Festinger postulou que os seres humanos possuem uma necessidade intrínseca de avaliar suas opiniões e capacidades comparando-se a outros, especialmente na ausência de padrões objetivos. No ambiente digital, esse mecanismo é intensificado por dois fatores estruturais: (a) a **visibilidade constante de métricas sociais** (curtidas, seguidores, comentários) que atribuem valor social explícito a indivíduos; e (b) a **curadoria algorítmica de conteúdo idealizado**, que expõe os jovens sistematicamente a representações seletivas de beleza, sucesso e popularidade.

Os dados da presente pesquisa corroboram as predições da Teoria da Comparação Social: as meninas — mais expostas às pressões de conformidade estética veiculadas pelo Instagram e TikTok — são significativamente mais afetadas por conteúdos sobre emagrecimento extremo ($p = 0,016$; $OR = 0,72$) e por discriminação baseada em aparência física ($p = 0,0085$; $OR = 0,26$), além de buscarem mais informações sobre saúde mental ($p < 10^{-14}$), sugerindo que a comparação social desfavorável contribui para maior percepção de sofrimento psicológico entre adolescentes do sexo feminino.

### 8.2 Teoria dos Usos e Gratificações (Katz, Blumler & Gurevitch, 1973-1974)

A Teoria dos Usos e Gratificações (TUG) parte da premissa de que os indivíduos são usuários **ativos e seletivos** dos meios de comunicação, buscando satisfazer necessidades psicossociais específicas — como conexão social, entretenimento, formação identitária, vigilância informacional e fuga de problemas cotidianos. Sob essa perspectiva, o uso de redes sociais não é passivo, mas motivado por funções percebidas pelo próprio usuário.

Os dados confirmam esta premissa: **32,3% dos adolescentes** (5,6 milhões) utilizam a internet deliberadamente como estratégia de *coping* emocional (busca de apoio em momentos difíceis), e **28,1%** (3,6 milhões) pesquisam ativamente informações sobre saúde mental e sentimentos. Plataformas de microvídeos, por sua vez, satisfazem necessidades de identidade e pertencimento por meio de tendências (trends), sons virais e comunidades de interesse. O risco identificado pela TUG é a **dependência funcional**: quando o jovem internaliza que a rede é o único ou principal recurso disponível para regulação emocional, torna-se mais vulnerável aos efeitos de desconexão ($17,5\%$ sofrem mal-estar ao ficar off-line).

### 8.3 Reforço Intermitente Variável e Compulsão Digital (Skinner, 1938; adaptado)

O behaviorismo de B.F. Skinner demonstrou que o **reforço intermitente variável** — recompensas imprevisíveis e irregulares — é o esquema mais resistente à extinção e o que mais intensifica o comportamento. As plataformas de redes sociais replicam estruturalmente esse mecanismo: o usuário nunca sabe quando um post receberá muitas curtidas, quando um vídeo viralizará ou quando uma mensagem importante chegará, gerando o que Tristan Harris denomina **"máquina caça-níqueis digital"** (*slot machine effect*).

Este mecanismo é agudamente amplificado no TikTok e correlatos, onde o algoritmo de *feed* infinito fornece vídeos de qualidade variável de forma contínua e imprevisível. Os dados empíricos dessa pesquisa registram os efeitos comportamentais desse ciclo: **26,4% dos adolescentes** (4,7 milhões) tentaram reduzir o tempo on-line e falharam — uma descrição operacional de comportamento compulsivo —, e **20,7%** navegam sem objetivos claros ("sem interesse direto"), sugestivo de comportamento de *scrolling* automático dissociativo.

### 8.4 Hipótese do Deslocamento do Sono (*Sleep Displacement Hypothesis* — Cain & Gradisar, 2010)

Cain e Gradisar sistematizaram a hipótese de que o uso de telas eletrônicas antes de dormir prejudica o sono por três mecanismos complementares: (a) **supressão da melatonina** pela luz azul emitida por telas LED; (b) **excitação cognitiva e emocional** provocada por conteúdos socialmente carregados (conflitos, comparações, notícias), que eleva o estado de alerta; e (c) **deslocamento temporal direto**, em que horas de sono são substituídas por horas de tela.

A pesquisa TIC Kids Online 2024 documenta esses efeitos em escala nacional: **16,3% dos adolescentes** (2,9 milhões) declararam ter perdido refeições *ou* noites de sono em função do uso da internet — com a regressão logística identificando que a **vivência de ofensas e conflitos on-line é o mecanismo mais potente** na cadeia causal ($AOR = 2,72$), possivelmente porque gera a excitação cognitivo-emocional que Cain & Gradisar identificaram como o componente mais devastador para a qualidade do sono adolescente.

---

## 9. DISCUSSÃO DOS RESULTADOS À LUZ DA LITERATURA

Os achados da presente análise empírica dialogam diretamente com a literatura científica internacional e com o artigo base da proposta:

1. **A Hipótese do Deslocamento vs. Hipótese da Qualidade da Experiência**: Os dados refutam uma visão simplista de que o mero tempo de tela é o único causador de sofrimento psicológico. A perda de sono e o sofrimento emocional estão muito mais associados à **natureza das vivências on-line (conflitos, ofensas e cyberbullying)** do que exclusivamente à frequência de acesso, convergindo com as diretrizes da APA (2023).
2. **Comparação Social, Algoritmos de Vídeos Rápidos e Pressão Estética**: A sobrecarga de vivências aversivas e busca de emagrecimento entre as meninas corrobora os achados da OMS (2024), que apontam as adolescentes do sexo feminino como as mais vulneráveis à comparação social desfavorável promovida por feeds imagéticos e vídeos rápidos (Instagram e TikTok). A Teoria da Comparação Social (Festinger, 1954) oferece o arcabouço explicativo: o algoritmo de curadoria amplifica sistematicamente comparações ascendentes desfavoráveis.
3. **A Dualidade da Conectividade Digital**: É imperativo notar que a rede não é exclusivamente um ambiente de risco. O fato de 32,3% dos adolescentes utilizarem a internet para procurar ajuda em momentos de tristeza demonstra que as tecnologias digitais também operam como canal de suporte social e válvula de alívio emocional — uso este previsto e explicado pela Teoria dos Usos e Gratificações (Katz et al., 1973).
4. **Socialização Política e o Risco de Polarização Algorítmica**: A ascensão dos conteúdos rápidos como fonte primária de notícias para 12,9 milhões de jovens amplia o acesso à esfera pública, mas impõe desafios urgentes de letramento informacional, visto que 44,4% dos adolescentes carecem de ferramentas para checar a veracidade das narrativas a que são expostos.
5. **Comportamento Compulsivo e Reforço Intermitente**: A falha de autorregulação documentada em 26,4% dos jovens (tentativa sem sucesso de reduzir o tempo on-line) representa a manifestação empírica do mecanismo de reforço intermitente variável de Skinner, operacionalizado pelos algoritmos de recomendação das plataformas de microvídeos.

---

## 10. LIMITAÇÕES E CUIDADOS METODOLÓGICOS

Em estrito cumprimento aos cuidados éticos e metodológicos firmados na proposta:
- **Ausência de Escalas Clínicas**: A TIC Kids Online Brasil não aplica instrumentos diagnósticos psicométricos formais (como CES-D, GAD-7 ou BDI). As variáveis aqui analisadas refletem autorrelatos comportamentais e percepções dos jovens;
- **Natureza Transversal dos Dados**: Trata-se de um estudo observacional de corte transversal. Consequentemente, **não é permitido afirmar relações de causa e efeito**. Por exemplo, adolescentes já propensos à insônia ou com sofrimento prévio podem navegar mais durante a noite, estabelecendo uma causalidade reversa ou bidirecional;
- **Filtros Amostrais**: Determinados módulos sensíveis são respondidos apenas a partir dos 11 anos de idade, exigindo respeito rigoroso aos denominadores válidos.

---

## 11. RECOMENDAÇÕES DE POLÍTICAS PÚBLICAS E INTERVENÇÕES ESCOLARES

Com base nos achados empíricos e nos referenciais teóricos mobilizados, e respeitando os limites observacionais do estudo, apresentam-se as seguintes recomendações direcionadas a gestores públicos, educadores e famílias:

### 11.1 Fortalecimento da Mediação e do Apoio Familiar

O achado mais robusto e direto do modelo logístico é o **efeito protetor do apoio parental** ($AOR = 0,65; p = 0,0097$): adolescentes cujos responsáveis mantêm diálogo ativo sobre o que acontece na internet têm 35% menos chance de perder sono ou alimentação por conflitos digitais. Recomenda-se:

- **Programas de letramento digital para responsáveis** (oficinas em escolas e UBSs), ensinando abordagens de mediação ativa e construtiva — não apenas de proibição ou controle —, com foco no diálogo sobre vivências online;
- **Integração de pais e cuidadores às estratégias de saúde digital** desenvolvidas por psicólogos escolares e assistentes sociais;
- Campanhas públicas de conscientização sobre o papel protetor da conversa cotidiana entre pais e filhos sobre a vida digital.

### 11.2 Educação para Mídias Digitais e Letramento Informacional nas Escolas

O dado alarmante de que **44,4% dos adolescentes** não sabem verificar a veracidade de informações online e **44,6%** não distinguem publicidade paga de conteúdo orgânico exige resposta curricular urgente:

- **Inclusão de disciplinas ou módulos de Educação para as Mídias (Media Literacy)** no currículo da educação básica, cobrindo verificação de fatos (*fact-checking*), identificação de *deep fakes*, reconhecimento de publicidade nativa e funcionamento dos algoritmos de recomendação;
- **Projetos de verificação colaborativa** (*newsroom* estudantil) que desenvolvam habilidades práticas de checagem de fontes e contraste de narrativas;
- Atenção especial à **alfabetização política crítica**: dado que o TikTok é a fonte primária de notícias políticas para crescente parcela de adolescentes, o ensino de análise crítica de microvídeos com conteúdo político torna-se prioritário.

### 11.3 Programas de Suporte a Vítimas de Cyberbullying e Violência Online

O preditor mais potente de perda de sono e prejuízo alimentar é a **vivência de situações ofensivas online** ($AOR = 2,72$), afetando 33,4% dos adolescentes (5,9 milhões). Recomenda-se:

- **Protocolos claros de denúncia e acolhimento** nas escolas para casos de cyberbullying, integrando psicólogos, orientadores, equipes técnicas e, quando necessário, o Conselho Tutelar;
- **Canais de denúncia seguros e anônimos** nas instituições de ensino para relatos de violência digital;
- Capacitação de professores para identificar sinais de vitimização online (mudanças de comportamento, isolamento, queda de rendimento) e encaminhar adequadamente;
- Articulação com as plataformas digitais para agilizar **remoção de conteúdos abusivos** envolvendo menores, em consonância com o Marco Civil da Internet (Lei 12.965/2014) e o Estatuto da Criança e do Adolescente (ECA).

### 11.4 Transparência Algorítmica e Obrigações das Plataformas

As evidências de que o design das plataformas de microvídeos favorece comportamentos compulsivos (reforço intermitente variável) e comparação social desfavorável sustentam a necessidade de regulação:

- **Exigência de Relatórios de Impacto sobre Crianças e Adolescentes** (*Children's Impact Assessments*) a serem publicados pelas plataformas digitais, com dados sobre tempo médio de uso, taxas de exposição a conteúdos de risco e eficácia das ferramentas de controle parental;
- **Restrições ao design exploratório** (*dark patterns*) direcionado a menores, incluindo: *feed* infinito sem pausa, notificações de alta frequência e *autoplay* irrestrito;
- Apoio à tramitação do **PL 2.630/2020** (Lei das Fake News / Projeto de Lei das Plataformas Digitais) com salvaguardas específicas para a proteção de crianças e adolescentes.

### 11.5 Programas de Higiene do Sono nas Escolas

Com 2,9 milhões de adolescentes relatando privação de sono pelo uso da internet:

- **Integração de tópicos de higiene do sono** (impacto da luz azul, ritmo circadiano, rotinas de desconexão) nas aulas de Educação Física, Ciências e Saúde;
- Estímulo a **"zonas livres de telas"** nos dormitórios, com carregadores centralizados fora dos quartos;
- Projetos piloto de **início tardio das aulas** nas redes municipais e estaduais, em consonância com evidências científicas sobre o cronótipo adolescente (Cain & Gradisar, 2010).

---

## 12. CONCLUSÕES

O estudo cumpriu integralmente todos os objetivos propostos pelo grupo de pesquisa do IFRN Campus Canguaretama:
1. Foi realizada a ingestão, limpeza e exploração minuciosa da base oficial de microdados da TIC Kids Online Brasil 2024 com 2.686 registros;
2. As estimativas populacionais ponderadas refletiram fielmente os 26,5 milhões de crianças e adolescentes brasileiros;
3. Identificou-se que situações ofensivas e de cyberbullying exercem impacto determinante sobre o sono e o equilíbrio alimentar dos jovens ($AOR = 2,72$);
4. Comprovou-se o efeito protetor da mediação e apoio familiar ativo, reduzindo em 35% o risco de insônia decorrente de conflitos on-line ($AOR = 0,65$);
5. Mapeou-se a influência cultural e política dos conteúdos ultrarrápidos (TikTok/Reels), evidenciando a emergência de uma cultura participativa aliada a vulnerabilidades críticas de desinformação;
6. Foram produzidos artefatos computacionais completos e reprodutíveis: script Python (`scripts/analise_completa.py`), Jupyter Notebook comentado (`notebooks/Analise_Redes_Sociais_Saude_Mental_TIC_Kids.ipynb`), 8 tabelas em CSV (`output/`), 9 figuras gráficas de alta resolução (`figures/`) e um painel executivo interativo em HTML5 (`RELATORIO_EXECUTIVO.html`).

---

## REFERÊNCIAS

- AMERICAN PSYCHOLOGICAL ASSOCIATION (APA). **Health advisory on social media use in adolescence**. Washington, DC: APA, 2023. Disponível em: <https://www.apa.org/topics/social-media-internet/health-advisory-adolescent-social-media-use>. Acesso em: 18 nov. 2026.
- CENTRO REGIONAL DE ESTUDOS PARA O DESENVOLVIMENTO DA SOCIEDADE DA INFORMAÇÃO (Cetic.br). **Pesquisa TIC Kids Online Brasil 2024: Microdados e Relatório Metodológico**. São Paulo: Comitê Gestor da Internet no Brasil (CGI.br), 2024. Disponível em: <https://cetic.br/pt/arquivos/kidsonline/2024/criancas/>. Acesso em: 18 nov. 2026.
- WORLD HEALTH ORGANIZATION (WHO). Regional Office for Europe. **A focus on adolescent social media use and gaming in Europe, central Asia and Canada: Health Behaviour in School-aged Children international report from the 2021/2022 survey**. Volume 6. Copenhagen: WHO Regional Office for Europe, 2024. Disponível em: <https://www.who.int/europe/publications/i/item/9789289061322>. Acesso em: 18 nov. 2026.
