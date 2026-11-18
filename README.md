# Análise de Dados: Redes Sociais, Conteúdos Rápidos e Saúde Mental de Jovens
**Instituto Federal do Rio Grande do Norte (IFRN) - Campus Canguaretama**  
**Curso Superior de Tecnologia em Sistemas para Internet**

**Autores:**
- José Guilherme da Silva Neto
- Pedro Henrique de Oliveira Querino
- João Batista do Nascimento Junior

---

## 📌 Visão Geral do Projeto
Este projeto implementa uma análise empírica, exploratória, inferencial e multivariada dos microdados oficiais da pesquisa **TIC Kids Online Brasil 2024** (Cetic.br / NIC.br). O estudo investiga o impacto do ecossistema digital sob três eixos integrados:
1. **Saúde Mental e Sono:** Perda de sono/alimentação, dependência, sofrimento por desconexão e o efeito protetor da mediação familiar;
2. **Influência Cultural dos Conteúdos Rápidos:** Produção de conteúdo autoral, trocas interculturais, estética e o papel do TikTok/Reels;
3. **Socialização Política e Cidadania:** Consumo de notícias por microvídeos, debate cívico, ativismo juvenil e vulnerabilidade a *fake news*.

---

## 📁 Estrutura de Diretórios e Arquivos

```text
Analise_de_dados/
│
├── data/                                      # Microdados oficiais e dicionário de variáveis
│   ├── microdados_2024.csv                    # Base completa com 2.686 participantes e 523 atributos
│   └── dicionario_variaveis_2024.xlsx         # Metadados e questionário da pesquisa
│
├── notebooks/                                 # Notebooks interativos
│   └── Analise_Redes_Sociais_Saude_Mental_TIC_Kids.ipynb  # Jupyter Notebook completo com regressão e visualizações
│
├── scripts/                                   # Scripts Python modulares
│   ├── download_data.py                       # Download dos microdados e documentação
│   └── analise_completa.py                    # Pipeline analítico completo (descritiva, multivariada e cultural)
│
├── figures/                                   # Gráficos em alta resolução (300 DPI)
│   ├── figura1_perfil_demografico.png         # Distribuição sociodemográfica
│   ├── figura2_atividades_e_redes.png         # Atividades on-line e plataformas
│   ├── figura3_impacto_bem_estar_sono.png     # Indicadores de rotina e sono
│   ├── figura4_cyberbullying_demografia.png   # Riscos por faixa etária e sexo
│   ├── figura5_comparacao_uso_intensivo.png   # Comparativo: Uso intensivo vs moderado
│   ├── figura6_matriz_correlacao.png          # Heatmap de associações
│   ├── figura7_forest_plot_regressao.png      # Forest Plot dos Odds Ratios Ajustados (AOR)
│   ├── figura8_efeito_protetor_familia.png    # Índice IUPT e Efeito Protetor Parental
│   └── figura9_cultura_politica_videos_rapidos.png # Cultura digital, política e desinformação
│
├── output/                                    # Tabelas consolidadas em CSV
│   ├── tabela1_perfil_demografico.csv         # Perfil amostral e populacional
│   ├── tabela2_atividades_online.csv          # Frequência de atividades
│   ├── tabela3_plataformas_sociais.csv        # Penetração das redes sociais
│   ├── tabela4_indicadores_bem_estar_sono.csv # Sono, alimentação e autorregulação
│   ├── tabela5_riscos_cyberbullying.csv       # Experiências aversivas e discriminação
│   ├── tabela6_testes_qui_quadrado.csv        # Testes qui-quadrado, p-valor e Odds Ratio
│   ├── tabela7_regressao_logistica_multivariada.csv # Modelo Logit com AOR e IC 95%
│   └── tabela8_cultura_politica_conteudos_rapidos.csv # Indicadores culturais e políticos
│
├── RELATORIO_FINAL_ANALISE_DE_DADOS.md        # Relatório acadêmico completo (normas ABNT)
├── RELATORIO_EXECUTIVO.html                   # Dashboard executivo autônomo em HTML5 com gráficos
└── README.md                                  # Este arquivo de instruções
```

---

## 🚀 Como Executar

### 1. Pré-requisitos
Certifique-se de possuir Python 3.10+ instalado com as bibliotecas:
```bash
python -m pip install pandas numpy scipy matplotlib seaborn openpyxl statsmodels scikit-learn
```

### 2. Executar a Análise Completa
Para rodar todo o pipeline de processamento estatístico e gerar automaticamente as 8 tabelas e 9 gráficos:
```bash
python scripts/analise_completa.py
```

### 3. Visualizar o Relatório Executivo
Abra o arquivo `RELATORIO_EXECUTIVO.html` em qualquer navegador web (Google Chrome, Firefox, Edge). Todas as imagens e tabelas estão embutidas em Base64.

### 4. Abrir o Jupyter Notebook
```bash
jupyter notebook notebooks/Analise_Redes_Sociais_Saude_Mental_TIC_Kids.ipynb
```

---

## 👥 Divisão Temática da Apresentação da Equipe

O painel executivo interativo ([RELATORIO_EXECUTIVO.html](file:///c:/Users/gu268/Projetos/Analise_de_dados/RELATORIO_EXECUTIVO.html)) foi reestruturado em **3 partes modulares**, atribuindo a cada integrante um eixo analítico completo com roteiro de fala e dados:

1. **Parte 1 — José Guilherme da Silva Neto:**
   - *Tema:* Estrutura Sociodemográfica, Conectividade e Penetração de Plataformas;
   - *Foco:* População representada de 26,5 milhões, amostragem vs ponderação oficial (`PESO`), atividades on-line e hegemonia do Instagram (94,8%) e WhatsApp (90,0%);
   - *Artefatos:* Tabela 1, Tabela 2, Tabela 3, Figura 1 e Figura 2.

2. **Parte 2 — Pedro Henrique de Oliveira Querino:**
   - *Tema:* Saúde Mental, Prejuízos no Sono, Uso Problemático e Modelagem Multivariada;
   - *Foco:* Privação de sono/refeições (16,3%), descontrole de tempo (26,4%), escore somativo IUPT (Alfa = 0,5213), Regressão Logística Múltipla ($AOR = 2,72$ para ofensas on-line) e comprovação do Efeito Protetor Parental ($AOR = 0,65$; proteção de 35%);
   - *Artefatos:* Tabela 4, Tabela 6, Tabela 7, Figura 3, Figura 5, Figura 6, Figura 7 (Forest Plot) e Figura 8 (Proteção Familiar).

3. **Parte 3 — João Batista do Nascimento Junior:**
   - *Tema:* Conteúdos Rápidos (TikTok/Reels), Cultura Participativa, Socialização Política e Fake News;
   - *Foco:* Uso diário de TikTok por 50,8% dos jovens (12,3 milhões), cultura autoral de vídeos (36,1%), notícias on-line (52,7%), explosão do debate político aos 15-17 anos (18,5%) e déficit de letramento crítico (44,4% não sabem checar fatos);
   - *Artefatos:* Tabela 5, Tabela 8, Figura 4 e Figura 9.

---

## 📊 Principais Resultados Científicos
- **População:** 2.686 jovens entrevistados representando **26,5 milhões** de crianças e adolescentes no Brasil.
- **Prejuízo no Sono:** **16,3% (2,9 milhões de jovens)** deixaram de comer ou dormir devido à internet.
- **Vivência de Ofensas:** Aumenta em **2,72 vezes** o risco de perda de sono/refeições ($AOR = 2,72; p < 10^{-9}$), sendo o preditor mais crítico mesmo após controle estatístico multivariado.
- **Proteção Familiar:** O diálogo e suporte ativo dos pais reduz em **35%** o risco de insônia decorrente de situações aversivas ($AOR = 0,65; p = 0,0097$).
- **Conteúdos Rápidos (TikTok/Shorts/Reels):**
  - **50,8% (12,3 milhões)** utilizam TikTok diariamente ou várias vezes ao dia;
  - Usuários intensivos têm **79% mais probabilidade ($OR = 1,79; p < 0,0001$)** de produzir conteúdos culturais próprios;
  - Usuários intensivos têm **83% mais chances ($OR = 1,83; p = 0,0001$)** de debater política e questões sociais;
  - **44,4% dos adolescentes** não sabem checar se uma informação on-line é verdadeira, expondo uma grave vulnerabilidade a desinformação e polarização algorítmica.

---


## 🎤 Roteiros de Apresentação

Sugestões de roteiro para a apresentação oral do relatório, organizadas por autor.

---

### 🟦 Parte 1 — José Guilherme

> "Olá a todos. Abro a nossa apresentação contextualizando o universo da pesquisa TIC Kids Online Brasil 2024. Nossa base possui 2.686 participantes que, com a aplicação dos pesos amostrais oficiais (PESO), representam com precisão estatística mais de 26,5 milhões de crianças e adolescentes no Brasil. O primeiro achado indispensável é a quase universalização da conectividade: 96,3% dos jovens já usam a internet. Como podemos observar na Figura 1, a distribuição reflete o equilíbrio demográfico nacional (50,9% meninos e 49,1% meninas), com forte concentração nas classes C e DE (87,3% da população) e a predominância do Sudeste e Nordeste."

> "Na Figura 2 e na Tabela de Atividades, destaco que as plataformas visuais e de mensagens dominam o ecossistema: o Instagram alcança 94,8% de penetração ponderada, o WhatsApp atinge 90,0% e o TikTok 75,3%. Mais de 71,4% dos adolescentes navegam de forma intensiva (mais de 1 vez ao dia). Passo a palavra ao Pedro, que detalhará como essa intensidade reverbera no sono e na saúde psicológica dos jovens."

---

### 🟥 Parte 2 — Pedro Henrique

> "Obrigado, José. O meu bloco analisa o impacto das experiências digitais na rotina somática e no bem-estar dos adolescentes de 11 a 17 anos (Módulo T). Constatamos que 16,3% dos jovens — cerca de 2,9 milhões de adolescentes — relatam ter deixado de comer ou dormir por causa da internet. Além disso, 26,4% vivenciam falha de autorregulação, tentando reduzir o tempo on-line sem conseguir. Como podemos observar na Figura 3 e na Figura 5, a navegação sem propósito e os conflitos familiares afetam quase um quarto dos jovens."

> "Mas a grande contribuição científica do nosso trabalho está na Regressão Logística Multivariada (Tabela 7 e Figura 7 - Forest Plot). Controlando por gênero, idade e classe social, demonstramos que vivenciar situações ofensivas on-line aumenta em 2,72 vezes a chance de perder o sono (AOR = 2,72; p < 10⁻⁹). Em contrapartida, provamos empiricamente o 'Buffer Effect': adolescentes cujos pais conversam e explicam incômodos digitais têm 35% menos risco de sofrer perda de sono (AOR = 0,65; p = 0,0097), ilustrado na Figura 8. Passo ao João, que explicará o papel dos conteúdos rápidos e da desinformação nesse cenário."

---

### 🟨 Parte 3 — João Batista

> "Obrigado, Pedro. O meu eixo fecha a nossa pesquisa conectando a saúde mental às transformações sociais mais recentes: a cultura dos conteúdos rápidos (TikTok, Reels e Shorts) e a socialização cívica da juventude. Identificamos que metade dos jovens (50,8%, mais de 12,2 milhões) utiliza o TikTok diariamente. Como demonstra a Figura 9, isso gera uma transformação cultural profunda: os jovens deixaram de ser passivos e tornaram-se produtores culturais (36,1% criam vídeos e textos próprios). Usuários frequentes de TikTok têm 79% mais probabilidade de produzir conteúdo autoral (OR = 1,79)."

> "No campo político, a internet virou a principal fonte informativa: 52,7% consomem notícias on-line (12,9 milhões), e os jovens com uso intensivo de vídeos rápidos debatem política 83% mais (OR = 1,83; p = 0,0001). Contudo, há um alerta urgente na Figura 9 e na Figura 4: 44,4% dos adolescentes não sabem checar a veracidade de notícias e 44,6% não distinguem publicidade disfarçada em vídeos de influenciadores. A velocidade desses formatos favorece a desinformação emocional e a polarização. Concluímos com as recomendações integradas da equipe."

## 📚 Referências
- Cetic.br / NIC.br (2024). Pesquisa TIC Kids Online Brasil 2024.
- American Psychological Association - APA (2023). Health Advisory on Social Media Use in Adolescence.
- World Health Organization - WHO (2024). A focus on adolescent social media use and gaming in Europe, central Asia and Canada.
