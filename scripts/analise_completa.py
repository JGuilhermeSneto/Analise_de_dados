"""
PROPOSTA DE ANÁLISE DE DADOS: REDES SOCIAIS E SAÚDE MENTAL DE JOVENS
INSTITUIÇÃO FEDERAL DO RIO GRANDE DO NORTE (IFRN) - CAMPUS CANGUARETAMA
CURSO SUPERIOR DE TECNOLOGIA EM SISTEMAS PARA INTERNET

Autores: José Guilherme da Silva Neto, Pedro Henrique de Oliveira Querino, João Batista do Nascimento Junior
Fonte de Dados: TIC Kids Online Brasil 2024 (Cetic.br / NIC.br)
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.metrics import roc_curve, roc_auc_score

# ---------------------------------------------------------
# 1. Configurações Globais de Ambiente e Visualização
# ---------------------------------------------------------
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#e0e0e0'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.7

os.makedirs("output", exist_ok=True)
os.makedirs("figures", exist_ok=True)

# ---------------------------------------------------------
# 2. Carga e Pré-Processamento dos Microdados
# ---------------------------------------------------------
print("Carregando microdados da TIC Kids Online Brasil 2024...")
csv_path = "data/microdados_2024.csv"
df_raw = pd.read_csv(csv_path, sep=';', decimal=',', low_memory=False)
print(f"Total de registros carregados: {len(df_raw)}")
print(f"Total de variáveis disponíveis: {len(df_raw.columns)}")

df = df_raw.copy()

# Mapeamento de variáveis demográficas
faixa_map = {
    1: "9 a 10 anos",
    2: "11 a 12 anos",
    3: "13 a 14 anos",
    4: "15 a 17 anos"
}
sexo_map = {
    1: "Masculino",
    2: "Feminino"
}
regiao_map = {
    1: "Sudeste",
    2: "Nordeste",
    3: "Sul",
    4: "Norte",
    5: "Centro-Oeste"
}
classe_map = {
    1: "Classe AB",
    2: "Classe C",
    3: "Classe DE"
}
raca_map = {
    1: "Branca",
    2: "Preta",
    3: "Parda",
    4: "Amarela",
    5: "Indígena"
}

df["FAIXA_ETARIA_DESC"] = df["FAIXA_ETARIA"].map(faixa_map)
df["SEXO_DESC"] = df["SEXO_KIDS"].map(sexo_map)
df["REGIAO_DESC"] = df["COD_REGIAO_2"].map(regiao_map)
df["CLASSE_DESC"] = df["CLASSE_2015_REC"].map(classe_map)
df["RACA_DESC"] = df["RACA_KIDS"].map(raca_map)

# Função auxiliar para limpar binários (1 = Sim, 0 = Não, outros = NaN)
def clean_binary(series):
    return series.apply(lambda x: 1 if x == 1 else (0 if x == 0 else np.nan))

# Variáveis comportamentais do Módulo T (11 a 17 anos)
df["PERDEU_SONO_COMIDA"] = clean_binary(df["T12_A"])
df["MAL_POR_DESCONECTAR"] = clean_binary(df["T12_B"])
df["NAVEGACAO_COMPULSIVA"] = clean_binary(df["T12_C"])
df["MENOS_TEMPO_FAMILIA_ESTUDO"] = clean_binary(df["T12_D"])
df["TENTOU_DIMINUIR_FALHOU"] = clean_binary(df["T12_E"])

# Experiências Negativas Gerais e Cyberbullying (11 a 17 anos)
df["EXP_NEGATIVA_GERAL"] = clean_binary(df["T0"])  # Aconteceu algo que não gostou, ofendeu ou chateou
df["CB_MENSAGEM_OFENSIVA"] = clean_binary(df["T2_A"])
df["CB_POSTAGEM_OFENSIVA"] = clean_binary(df["T2_B"])
df["CB_EXCLUSAO_GRUPO"] = clean_binary(df["T2_C"])
df["CB_AMEACA"] = clean_binary(df["T2_D"])
df["CB_AUTORIA"] = clean_binary(df["T3"])

# Indicador agregado de vitimização por cyberbullying (se sofreu pelo menos 1 das 4 agressões)
cb_cols = ["CB_MENSAGEM_OFENSIVA", "CB_POSTAGEM_OFENSIVA", "CB_EXCLUSAO_GRUPO", "CB_AMEACA"]
# Apenas para quem respondeu ao módulo T (tem pelo menos uma resposta não nula)
df["CB_VITIMA_QUALQUER"] = df[cb_cols].apply(
    lambda r: 1 if any(r == 1) else (0 if (r == 0).all() else np.nan), axis=1
)

# Discriminação e Saúde Mental
df["DISCRIMINACAO_GERAL"] = clean_binary(df["T20"])
df["DISCRIMINACAO_APARENCIA"] = clean_binary(df["T21_G"])
df["CONTEUDO_AUTOMUTILACAO"] = clean_binary(df["T10_A"])
df["CONTEUDO_SUICIDIO"] = clean_binary(df["T10_B"])
df["CONTEUDO_EMAGRECIMENTO"] = clean_binary(df["T10_C"])
df["CONTEUDO_VIOLENCIA"] = clean_binary(df["T10_F"])

df["INFO_SAUDE_MENTAL"] = clean_binary(df["T23_E"])
df["BUSCOU_AJUDA_EMOCIONAL"] = clean_binary(df["T25"])

# Redes Sociais e Atividades Gerais
df["USA_REDES_SOCIAIS"] = clean_binary(df["N1_G1"])
# Frequência de uso de redes sociais: 1="Mais de uma vez por dia", 2="1x/dia", etc.
df["USO_INTENSIVO_REDES"] = df["N2_G1"].apply(lambda x: 1 if x == 1 else (0 if x in [2, 3, 4, 5] else np.nan))

# Plataformas de Redes Sociais no Módulo O
df["TEM_WHATSAPP"] = clean_binary(df["O7_E"])
df["TEM_INSTAGRAM"] = clean_binary(df["O7_B"])
df["TEM_TIKTOK"] = clean_binary(df["O7_D"])
df["TEM_YOUTUBE"] = clean_binary(df["O7_F"])
df["TEM_FACEBOOK"] = clean_binary(df["O7_A"])
df["TEM_DISCORD"] = clean_binary(df["O7_G"])

# Atividades gerais
df["ATIVIDADE_VIDEOS"] = clean_binary(df["N1_E1"])
df["ATIVIDADE_MUSICA"] = clean_binary(df["N1_F1"])
df["ATIVIDADE_MENSAGENS"] = clean_binary(df["N1_H"])
df["ATIVIDADE_PESQUISA_ESCOLA"] = clean_binary(df["N1_C"])
df["ATIVIDADE_JOGOS"] = clean_binary(df["N1_I"])
df["ATIVIDADE_POSTAR_FOTO_PROPRIA"] = clean_binary(df["N1_1_Q"])

# ---------------------------------------------------------
# 3. Funções Estatísticas (Ponderadas e Testes de Associação)
# ---------------------------------------------------------
def weighted_mean(series, weights):
    valid = series.notna() & weights.notna()
    if valid.sum() == 0:
        return np.nan
    return np.average(series[valid], weights=weights[valid])

def weighted_stats_table(df_subset, col_name, weight_col="PESO"):
    n_total = df_subset[col_name].notna().sum()
    pct_unweighted = (df_subset[col_name] == 1).mean() * 100
    pct_weighted = weighted_mean(df_subset[col_name], df_subset[weight_col]) * 100
    pop_estimada = (df_subset[col_name] == 1).astype(float) * df_subset[weight_col]
    pop_estimada_total = pop_estimada.sum()
    return {
        "N_Amostral_Valido": int(n_total),
        "Pct_Nao_Ponderado": round(pct_unweighted, 2),
        "Pct_Ponderado": round(pct_weighted, 2),
        "Populacao_Estimada": int(pop_estimada_total)
    }

def chi2_analysis(df_data, var_x, var_y):
    ct = pd.crosstab(df_data[var_x], df_data[var_y])
    chi2, p_val, dof, expected = stats.chi2_contingency(ct)
    n = ct.to_numpy().sum()
    min_dim = min(ct.shape) - 1
    cramer_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 and n > 0 else 0
    
    # Se for 2x2, calcula Odds Ratio
    odds_ratio, p_or = np.nan, np.nan
    if ct.shape == (2, 2):
        odds_ratio, p_or = stats.fisher_exact(ct)
        
    return {
        "Contingency_Table": ct,
        "Chi2": round(chi2, 4),
        "p_value": p_val,
        "dof": dof,
        "Cramer_V": round(cramer_v, 4),
        "Odds_Ratio": round(odds_ratio, 4) if not np.isnan(odds_ratio) else np.nan
    }

# ---------------------------------------------------------
# 4. Geração dos Resultados Analíticos e Tabelas
# ---------------------------------------------------------
print("\n--- 4.1 Caracterização Demográfica da População ---")
demo_summary = []
for var, desc in [
    ("FAIXA_ETARIA_DESC", "Faixa Etária"),
    ("SEXO_DESC", "Sexo"),
    ("REGIAO_DESC", "Região Geográfica"),
    ("CLASSE_DESC", "Classe Socioeconômica"),
    ("RACA_DESC", "Cor / Raça")
]:
    grouped = df.groupby(var, observed=False).apply(
        lambda g: pd.Series({
            "Amostra (N)": len(g),
            "Amostra (%)": round(len(g) / len(df) * 100, 2),
            "População Estimada": int(g["PESO"].sum()),
            "População (%)": round(g["PESO"].sum() / df["PESO"].sum() * 100, 2)
        })
    )
    grouped["Variavel"] = desc
    demo_summary.append(grouped.reset_index().rename(columns={var: "Categoria"}))

df_demo_all = pd.concat(demo_summary, ignore_index=True)
df_demo_all.to_csv("output/tabela1_perfil_demografico.csv", index=False, encoding='utf-8-sig')
print("Tabela 1 salva em output/tabela1_perfil_demografico.csv")

print("\n--- 4.2 Hábitos de Conectividade e Atividades On-line ---")
atividades = [
    ("ATIVIDADE_VIDEOS", "Assistir vídeos/filmes"),
    ("ATIVIDADE_MUSICA", "Ouvir música on-line"),
    ("ATIVIDADE_MENSAGENS", "Enviar mensagens instantâneas"),
    ("USA_REDES_SOCIAIS", "Usar redes sociais (geral)"),
    ("USO_INTENSIVO_REDES", "Uso intensivo de redes (> 1x/dia)"),
    ("ATIVIDADE_PESQUISA_ESCOLA", "Pesquisar trabalhos escolares"),
    ("ATIVIDADE_JOGOS", "Jogar on-line"),
    ("ATIVIDADE_POSTAR_FOTO_PROPRIA", "Postar foto/vídeo onde aparece")
]

ativ_res = []
for col, label in atividades:
    res = weighted_stats_table(df, col)
    res["Atividade"] = label
    ativ_res.append(res)
df_ativ = pd.DataFrame(ativ_res)[["Atividade", "N_Amostral_Valido", "Pct_Nao_Ponderado", "Pct_Ponderado", "Populacao_Estimada"]]
df_ativ.to_csv("output/tabela2_atividades_online.csv", index=False, encoding='utf-8-sig')
print("Tabela 2 salva em output/tabela2_atividades_online.csv")

print("\n--- 4.3 Penetração das Plataformas de Redes Sociais ---")
plataformas = [
    ("TEM_WHATSAPP", "WhatsApp"),
    ("TEM_INSTAGRAM", "Instagram"),
    ("TEM_TIKTOK", "TikTok"),
    ("TEM_YOUTUBE", "YouTube"),
    ("TEM_FACEBOOK", "Facebook"),
    ("TEM_DISCORD", "Discord")
]

plat_res = []
# Usuários de internet no questionário (D1 == 1)
df_net_users = df[df["D1"] == 1]
for col, label in plataformas:
    res = weighted_stats_table(df_net_users, col)
    res["Plataforma"] = label
    plat_res.append(res)
df_plat = pd.DataFrame(plat_res)[["Plataforma", "N_Amostral_Valido", "Pct_Nao_Ponderado", "Pct_Ponderado", "Populacao_Estimada"]]
df_plat.to_csv("output/tabela3_plataformas_sociais.csv", index=False, encoding='utf-8-sig')
print("Tabela 3 salva em output/tabela3_plataformas_sociais.csv")

print("\n--- 4.4 Indicadores de Uso Problemático e Reflexos no Bem-Estar / Sono (11 a 17 anos) ---")
# Filtro oficial do Módulo T: adolescentes de 11 a 17 anos usuários de internet (IDADE_INTERNET == 1)
df_teens = df[df["IDADE_INTERNET"] == 1].copy()
print(f"Adolescentes no Módulo T (11 a 17 anos): N = {len(df_teens)}")

bem_estar_vars = [
    ("PERDEU_SONO_COMIDA", "Deixou de comer ou dormir por causa da internet"),
    ("MAL_POR_DESCONECTAR", "Sentiu-se mal por não poder estar conectado"),
    ("MENOS_TEMPO_FAMILIA_ESTUDO", "Passou menos tempo com família, amigos ou estudos"),
    ("TENTOU_DIMINUIR_FALHOU", "Tentou passar menos tempo e não conseguiu"),
    ("NAVEGACAO_COMPULSIVA", "Navegação compulsiva/sem interesse direto"),
    ("INFO_SAUDE_MENTAL", "Buscou informações sobre saúde mental / sentimentos"),
    ("BUSCOU_AJUDA_EMOCIONAL", "Usou internet para buscar ajuda em momentos difíceis")
]

be_res = []
for col, label in bem_estar_vars:
    res = weighted_stats_table(df_teens, col)
    res["Indicador"] = label
    be_res.append(res)
df_be = pd.DataFrame(be_res)[["Indicador", "N_Amostral_Valido", "Pct_Nao_Ponderado", "Pct_Ponderado", "Populacao_Estimada"]]
df_be.to_csv("output/tabela4_indicadores_bem_estar_sono.csv", index=False, encoding='utf-8-sig')
print("Tabela 4 salva em output/tabela4_indicadores_bem_estar_sono.csv")

print("\n--- 4.5 Riscos On-line, Cyberbullying e Discriminação (11 a 17 anos) ---")
risco_vars = [
    ("EXP_NEGATIVA_GERAL", "Passou por situação desagradável/ofensiva (T0)"),
    ("CB_MENSAGEM_OFENSIVA", "Recebeu mensagens ofensivas"),
    ("CB_POSTAGEM_OFENSIVA", "Teve ofensas postadas publicamente"),
    ("CB_EXCLUSAO_GRUPO", "Foi excluído(a) de grupos ou atividades on-line"),
    ("CB_AMEACA", "Foi ameaçado(a) na internet"),
    ("CB_VITIMA_QUALQUER", "Vitimização por Cyberbullying (consolidado)"),
    ("CB_AUTORIA", "Praticou cyberbullying contra outrem"),
    ("DISCRIMINACAO_GERAL", "Sofreu discriminação on-line"),
    ("DISCRIMINACAO_APARENCIA", "Sofreu discriminação por aparência física"),
    ("CONTEUDO_EMAGRECIMENTO", "Exposto(a) a formas de ficar muito magro(a)"),
    ("CONTEUDO_AUTOMUTILACAO", "Exposto(a) a formas de se machucar fisicamente"),
    ("CONTEUDO_SUICIDIO", "Exposto(a) a formas de cometer suicídio"),
    ("CONTEUDO_VIOLENCIA", "Exposto(a) a cenas de violência ou muito sangue")
]

risco_res = []
for col, label in risco_vars:
    res = weighted_stats_table(df_teens, col)
    res["Experiência de Risco"] = label
    risco_res.append(res)
df_risco = pd.DataFrame(risco_res)[["Experiência de Risco", "N_Amostral_Valido", "Pct_Nao_Ponderado", "Pct_Ponderado", "Populacao_Estimada"]]
df_risco.to_csv("output/tabela5_riscos_cyberbullying.csv", index=False, encoding='utf-8-sig')
print("Tabela 5 salva em output/tabela5_riscos_cyberbullying.csv")

# ---------------------------------------------------------
# 5. Cruzamentos Estatísticos e Testes de Hipótese (Chi-quadrado)
# ---------------------------------------------------------
print("\n--- 5.1 Testes de Associação Estatística (Chi-Quadrado) ---")
test_pairs = [
    # Relação de Redes Intensivas com Desfechos Comportamentais
    ("USO_INTENSIVO_REDES", "EXP_NEGATIVA_GERAL", "Uso Intensivo de Redes Sociais x Situação Ofensiva/Desagradável (T0)"),
    ("USO_INTENSIVO_REDES", "PERDEU_SONO_COMIDA", "Uso Intensivo de Redes Sociais x Perda de Sono/Refeições"),
    ("USO_INTENSIVO_REDES", "MAL_POR_DESCONECTAR", "Uso Intensivo de Redes Sociais x Sofrimento por Desconexão"),
    ("USO_INTENSIVO_REDES", "MENOS_TEMPO_FAMILIA_ESTUDO", "Uso Intensivo de Redes Sociais x Prejuízo Familiar/Escolar"),
    ("USO_INTENSIVO_REDES", "TENTOU_DIMINUIR_FALHOU", "Uso Intensivo de Redes Sociais x Falha de Autorregulação"),
    # Relação de Experiência Negativa / Cyberbullying com Sono e Bem-Estar
    ("EXP_NEGATIVA_GERAL", "PERDEU_SONO_COMIDA", "Situação Ofensiva/Desagradável (T0) x Perda de Sono/Refeições"),
    ("EXP_NEGATIVA_GERAL", "MAL_POR_DESCONECTAR", "Situação Ofensiva/Desagradável (T0) x Sofrimento por Desconexão"),
    ("EXP_NEGATIVA_GERAL", "TENTOU_DIMINUIR_FALHOU", "Situação Ofensiva/Desagradável (T0) x Falha de Autorregulação"),
    # Diferenças por Sexo
    ("SEXO_DESC", "DISCRIMINACAO_APARENCIA", "Sexo x Discriminação por Aparência Física"),
    ("SEXO_DESC", "CONTEUDO_EMAGRECIMENTO", "Sexo x Exposição a Conteúdos de Emagrecimento Extremo"),
    ("SEXO_DESC", "INFO_SAUDE_MENTAL", "Sexo x Procura de Informações sobre Saúde Mental"),
    ("SEXO_DESC", "EXP_NEGATIVA_GERAL", "Sexo x Situação Ofensiva/Desagradável (T0)"),
    # Diferenças por Faixa Etária
    ("FAIXA_ETARIA_DESC", "EXP_NEGATIVA_GERAL", "Faixa Etária x Situação Ofensiva/Desagradável (T0)"),
    ("FAIXA_ETARIA_DESC", "PERDEU_SONO_COMIDA", "Faixa Etária x Perda de Sono/Refeições")
]

chi2_results = []
for vx, vy, label in test_pairs:
    sub_test = df_teens[[vx, vy]].dropna()
    res = chi2_analysis(sub_test, vx, vy)
    chi2_results.append({
        "Relação Analisada": label,
        "N": len(sub_test),
        "Chi2": res["Chi2"],
        "Graus de Liberdade": res["dof"],
        "p-valor": f"{res['p_value']:.4e}" if res['p_value'] < 0.001 else f"{res['p_value']:.4f}",
        "V de Cramér": res["Cramer_V"],
        "Odds Ratio (OR)": res["Odds_Ratio"] if not np.isnan(res["Odds_Ratio"]) else "N/A",
        "Significativo (p < 0.05)": "Sim" if res["p_value"] < 0.05 else "Não"
    })

df_chi2 = pd.DataFrame(chi2_results)
df_chi2.to_csv("output/tabela6_testes_qui_quadrado.csv", index=False, encoding='utf-8-sig')
print("Tabela 6 salva em output/tabela6_testes_qui_quadrado.csv")
print(df_chi2.to_string())

# ---------------------------------------------------------
# 6. Produção dos Gráficos de Visualização (300 DPI)
# ---------------------------------------------------------
print("\n--- 6. Gerando Figuras Gráficas ---")

# FIGURA 1: Perfil Demográfico da População Pesquisada
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
palette = sns.color_palette("mako", 6)

# 1.1 Faixa Etária
df_faixa = df.groupby("FAIXA_ETARIA_DESC", observed=False)["PESO"].sum().reset_index()
df_faixa["Pct"] = df_faixa["PESO"] / df_faixa["PESO"].sum() * 100
sns.barplot(data=df_faixa, x="FAIXA_ETARIA_DESC", y="Pct", ax=axes[0, 0], palette="Blues_d")
axes[0, 0].set_title("Distribuição Populacional por Faixa Etária", fontsize=12, fontweight='bold', pad=10)
axes[0, 0].set_xlabel("Faixa Etária", fontsize=10)
axes[0, 0].set_ylabel("Percentual (%) Ponderado", fontsize=10)
for p in axes[0, 0].patches:
    axes[0, 0].annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='bottom', fontsize=9, xytext=(0, 3), textcoords='offset points')

# 1.2 Sexo
df_sexo = df.groupby("SEXO_DESC", observed=False)["PESO"].sum().reset_index()
df_sexo["Pct"] = df_sexo["PESO"] / df_sexo["PESO"].sum() * 100
sns.barplot(data=df_sexo, x="SEXO_DESC", y="Pct", ax=axes[0, 1], palette="crest")
axes[0, 1].set_title("Distribuição Populacional por Sexo", fontsize=12, fontweight='bold', pad=10)
axes[0, 1].set_xlabel("Sexo", fontsize=10)
axes[0, 1].set_ylabel("Percentual (%) Ponderado", fontsize=10)
for p in axes[0, 1].patches:
    axes[0, 1].annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='bottom', fontsize=9, xytext=(0, 3), textcoords='offset points')

# 1.3 Região
df_reg = df.groupby("REGIAO_DESC", observed=False)["PESO"].sum().reset_index().sort_values(by="PESO", ascending=False)
df_reg["Pct"] = df_reg["PESO"] / df_reg["PESO"].sum() * 100
sns.barplot(data=df_reg, x="REGIAO_DESC", y="Pct", ax=axes[1, 0], palette="viridis")
axes[1, 0].set_title("Distribuição por Região Geográfica", fontsize=12, fontweight='bold', pad=10)
axes[1, 0].set_xlabel("Região", fontsize=10)
axes[1, 0].set_ylabel("Percentual (%) Ponderado", fontsize=10)
for p in axes[1, 0].patches:
    axes[1, 0].annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='bottom', fontsize=9, xytext=(0, 3), textcoords='offset points')

# 1.4 Classe Social
df_classe = df.groupby("CLASSE_DESC", observed=False)["PESO"].sum().reset_index()
df_classe["Pct"] = df_classe["PESO"] / df_classe["PESO"].sum() * 100
sns.barplot(data=df_classe, x="CLASSE_DESC", y="Pct", ax=axes[1, 1], palette="magma")
axes[1, 1].set_title("Distribuição por Classe Socioeconômica", fontsize=12, fontweight='bold', pad=10)
axes[1, 1].set_xlabel("Classe Social", fontsize=10)
axes[1, 1].set_ylabel("Percentual (%) Ponderado", fontsize=10)
for p in axes[1, 1].patches:
    axes[1, 1].annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='bottom', fontsize=9, xytext=(0, 3), textcoords='offset points')

plt.suptitle("Figura 1: Caracterização Sociodemográfica da População (TIC Kids Online Brasil 2024)", fontsize=14, fontweight='bold', y=0.99)
plt.tight_layout()
plt.savefig("figures/figura1_perfil_demografico.png", dpi=300)
plt.close()
print("Figura 1 salva em figures/figura1_perfil_demografico.png")

# FIGURA 2: Hábitos e Plataformas de Redes Sociais
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

df_ativ_plot = df_ativ.sort_values(by="Pct_Ponderado", ascending=True)
sns.barplot(data=df_ativ_plot, y="Atividade", x="Pct_Ponderado", ax=ax1, palette="flare")
ax1.set_title("Atividades On-line mais Frequentes (Últimos 3 Meses)", fontsize=12, fontweight='bold', pad=10)
ax1.set_xlabel("Proporção (%) Ponderada", fontsize=10)
ax1.set_ylabel("")
for p in ax1.patches:
    ax1.annotate(f"{p.get_width():.1f}%", (p.get_width(), p.get_y() + p.get_height() / 2.),
                 ha='left', va='center', fontsize=9, xytext=(4, 0), textcoords='offset points')

df_plat_plot = df_plat.sort_values(by="Pct_Ponderado", ascending=True)
sns.barplot(data=df_plat_plot, y="Plataforma", x="Pct_Ponderado", ax=ax2, palette="crest")
ax2.set_title("Penetração de Redes Sociais e Mensageiros (9 a 17 anos)", fontsize=12, fontweight='bold', pad=10)
ax2.set_xlabel("Proporção (%) Ponderada", fontsize=10)
ax2.set_ylabel("")
for p in ax2.patches:
    ax2.annotate(f"{p.get_width():.1f}%", (p.get_width(), p.get_y() + p.get_height() / 2.),
                 ha='left', va='center', fontsize=9, xytext=(4, 0), textcoords='offset points')

plt.suptitle("Figura 2: Hábitos Digitais e Penetração de Plataformas On-line", fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig("figures/figura2_atividades_e_redes.png", dpi=300)
plt.close()
print("Figura 2 salva em figures/figura2_atividades_e_redes.png")

# FIGURA 3: Prevalência de Indicadores de Uso Problemático e Sono (11 a 17 anos)
fig, ax = plt.subplots(figsize=(10, 6))
df_be_plot = df_be.sort_values(by="Pct_Ponderado", ascending=True)
sns.barplot(data=df_be_plot, y="Indicador", x="Pct_Ponderado", ax=ax, palette="rocket")
ax.set_title("Indicadores de Uso Problemático, Impacto na Rotina e Apoio Emocional (11 a 17 anos)", fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel("Percentual (%) Ponderado", fontsize=10)
ax.set_ylabel("")
for p in ax.patches:
    ax.annotate(f"{p.get_width():.1f}%", (p.get_width(), p.get_y() + p.get_height() / 2.),
                 ha='left', va='center', fontsize=9, xytext=(5, 0), textcoords='offset points')

plt.tight_layout()
plt.savefig("figures/figura3_impacto_bem_estar_sono.png", dpi=300)
plt.close()
print("Figura 3 salva em figures/figura3_impacto_bem_estar_sono.png")

# FIGURA 4: Experiências de Risco e Vulnerabilidade por Faixa Etária e Sexo
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Experiências Negativas (T0) por Faixa Etária
exp_by_age = df_teens.groupby("FAIXA_ETARIA_DESC", observed=False).apply(
    lambda g: weighted_mean(g["EXP_NEGATIVA_GERAL"], g["PESO"]) * 100
).reset_index().rename(columns={0: "Pct_Exp"})
sns.barplot(data=exp_by_age, x="FAIXA_ETARIA_DESC", y="Pct_Exp", ax=ax1, palette="mako")
ax1.set_title("Vivência de Situações Desagradáveis/Ofensivas por Faixa Etária (11 a 17 anos)", fontsize=11, fontweight='bold', pad=10)
ax1.set_xlabel("Faixa Etária", fontsize=10)
ax1.set_ylabel("Prevalência (%) Ponderada", fontsize=10)
for p in ax1.patches:
    ax1.annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height()),
                 ha='center', va='bottom', fontsize=9, xytext=(0, 3), textcoords='offset points')

# Discriminação por Aparência Física e Exposição a Conteúdos de Emagrecimento por Sexo
sex_comp = []
for s in ["Masculino", "Feminino"]:
    sub_s = df_teens[df_teens["SEXO_DESC"] == s]
    p_exp = weighted_mean(sub_s["EXP_NEGATIVA_GERAL"], sub_s["PESO"]) * 100
    p_emagr = weighted_mean(sub_s["CONTEUDO_EMAGRECIMENTO"], sub_s["PESO"]) * 100
    p_sono = weighted_mean(sub_s["PERDEU_SONO_COMIDA"], sub_s["PESO"]) * 100
    sex_comp.append({"Sexo": s, "Indicador": "Situação Desagradável/Ofensiva", "Pct": p_exp})
    sex_comp.append({"Sexo": s, "Indicador": "Viu Conteúdo Emagrecimento", "Pct": p_emagr})
    sex_comp.append({"Sexo": s, "Indicador": "Perdeu Sono / Refeição", "Pct": p_sono})
df_sex_comp = pd.DataFrame(sex_comp)

sns.barplot(data=df_sex_comp, x="Indicador", y="Pct", hue="Sexo", ax=ax2, palette="Set2")
ax2.set_title("Vulnerabilidades Digitais Comparadas por Sexo (11 a 17 anos)", fontsize=11, fontweight='bold', pad=10)
ax2.set_xlabel("")
ax2.set_ylabel("Percentual (%) Ponderado", fontsize=10)
ax2.tick_params(axis='x', rotation=10)
for p in ax2.patches:
    if p.get_height() > 0:
        ax2.annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='bottom', fontsize=8, xytext=(0, 3), textcoords='offset points')

plt.suptitle("Figura 4: Experiências de Risco e Vulnerabilidade Digital por Demografia", fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig("figures/figura4_cyberbullying_demografia.png", dpi=300)
plt.close()
print("Figura 4 salva em figures/figura4_cyberbullying_demografia.png")

# FIGURA 5: Comparação - Uso Intensivo de Redes (>1x/dia) vs Uso Moderado/Não Intensivo
comp_vars = [
    ("EXP_NEGATIVA_GERAL", "Situação Ofensiva"),
    ("PERDEU_SONO_COMIDA", "Perdeu Sono/Refeição"),
    ("MAL_POR_DESCONECTAR", "Mal-estar Desconexão"),
    ("TENTOU_DIMINUIR_FALHOU", "Falha Autorregulação"),
    ("MENOS_TEMPO_FAMILIA_ESTUDO", "Menos Tempo Família/Estudo")
]

comp_data = []
for col, lbl in comp_vars:
    # Intensivo
    sub_int = df_teens[df_teens["USO_INTENSIVO_REDES"] == 1]
    pct_int = weighted_mean(sub_int[col], sub_int["PESO"]) * 100
    # Não intensivo
    sub_mod = df_teens[df_teens["USO_INTENSIVO_REDES"] == 0]
    pct_mod = weighted_mean(sub_mod[col], sub_mod["PESO"]) * 100
    
    comp_data.append({"Indicador": lbl, "Grupo": "Uso Intensivo (>1x/dia)", "Percentual": pct_int})
    comp_data.append({"Indicador": lbl, "Grupo": "Uso Moderado/Esporádico", "Percentual": pct_mod})

df_comp = pd.DataFrame(comp_data)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=df_comp, x="Indicador", y="Percentual", hue="Grupo", ax=ax, palette=["#d95f02", "#1f78b4"])
ax.set_title("Figura 5: Desfechos de Rotina e Bem-Estar Segundo a Intensidade do Uso de Redes Sociais", fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel("")
ax.set_ylabel("Proporção Ponderada (%)", fontsize=11)
ax.set_ylim(0, max(df_comp["Percentual"]) * 1.25)
for p in ax.patches:
    if p.get_height() > 0:
        ax.annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom', fontsize=9, fontweight='bold', xytext=(0, 4), textcoords='offset points')

plt.tight_layout()
plt.savefig("figures/figura5_comparacao_uso_intensivo.png", dpi=300)
plt.close()
print("Figura 5 salva em figures/figura5_comparacao_uso_intensivo.png")

# FIGURA 6: Matriz de Correlação / Associação entre Indicadores
matrix_vars = [
    "USO_INTENSIVO_REDES",
    "EXP_NEGATIVA_GERAL",
    "PERDEU_SONO_COMIDA",
    "MAL_POR_DESCONECTAR",
    "MENOS_TEMPO_FAMILIA_ESTUDO",
    "TENTOU_DIMINUIR_FALHOU",
    "DISCRIMINACAO_GERAL",
    "INFO_SAUDE_MENTAL"
]

labels_matrix = [
    "Uso Intensivo Redes",
    "Exp. Negativa/Ofensa",
    "Perdeu Sono/Comida",
    "Mal Desconexão",
    "Menos Tempo Família",
    "Falha Regulação",
    "Sofreu Discriminação",
    "Buscou Saúde Mental"
]

corr_matrix = df_teens[matrix_vars].corr(method='pearson')
corr_matrix.columns = labels_matrix
corr_matrix.index = labels_matrix

fig, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(
    corr_matrix,
    annot=True,
    fmt=".2f",
    cmap="RdBu_r",
    vmin=-1,
    vmax=1,
    center=0,
    linewidths=0.8,
    linecolor="white",
    square=True,
    cbar_kws={"label": "Coeficiente de correlacao"},
    annot_kws={"size": 9},
    ax=ax
)
ax.set_title("Matriz de Correlacao entre Indicadores de Uso Digital e Bem-Estar",
             fontsize=14, fontweight="bold", pad=16)
ax.tick_params(axis="x", rotation=35)
ax.tick_params(axis="y", rotation=0)
for tick in ax.get_xticklabels():
    tick.set_horizontalalignment("right")
fig.tight_layout()
plt.savefig("figures/figura6_matriz_correlacao.png", dpi=300)
plt.close()
print("Figura 6 salva em figures/figura6_matriz_correlacao.png")

# ---------------------------------------------------------
# 7. Modelagem Estatística Multivariada (Regressão Logística Múltipla)
# ---------------------------------------------------------
print("\n--- 7.1 Regressão Logística Multivariada: Determinantes da Perda de Sono/Refeição ---")
df_reg = df_teens.copy()
df_reg["SEXO_FEM"] = df_reg["SEXO_KIDS"].apply(lambda x: 1 if x == 2 else 0)
df_reg["IDADE_13_14"] = (df_reg["FAIXA_ETARIA"] == 3).astype(int)
df_reg["IDADE_15_17"] = (df_reg["FAIXA_ETARIA"] == 4).astype(int)
df_reg["CLASSE_DE"] = (df_reg["CLASSE_2015_REC"] == 3).astype(int)
# Mediação Parental: pais ajudam ou explicam quando algo chateia (1="Sempre", 2="Quase sempre")
df_reg["APOIO_PAIS"] = df_reg["U6_E"].apply(lambda x: 1 if x in [1, 2] else (0 if x in [3, 4, 5] else np.nan))

formula_sono = "PERDEU_SONO_COMIDA ~ EXP_NEGATIVA_GERAL + USO_INTENSIVO_REDES + SEXO_FEM + IDADE_13_14 + IDADE_15_17 + CLASSE_DE + APOIO_PAIS"
data_reg_sono = df_reg[["PERDEU_SONO_COMIDA", "EXP_NEGATIVA_GERAL", "USO_INTENSIVO_REDES", "SEXO_FEM", "IDADE_13_14", "IDADE_15_17", "CLASSE_DE", "APOIO_PAIS"]].dropna()

logit_sono = smf.logit(formula=formula_sono, data=data_reg_sono).fit(disp=False)
params_s = logit_sono.params
conf_s = logit_sono.conf_int()
conf_s['OR'] = params_s
conf_s.columns = ['IC_2.5', 'IC_97.5', 'OR']
df_or_sono = np.exp(conf_s)[['OR', 'IC_2.5', 'IC_97.5']]
df_or_sono['p_value'] = logit_sono.pvalues
df_or_sono['coef'] = params_s
df_or_sono['std_err'] = logit_sono.bse

label_dict = {
    "Intercept": "Intercepto",
    "EXP_NEGATIVA_GERAL": "Vivenciou Ofensa/Desprazer On-line (T0)",
    "USO_INTENSIVO_REDES": "Uso Intensivo de Redes (>1x/dia)",
    "SEXO_FEM": "Sexo Feminino",
    "IDADE_13_14": "Faixa 13 a 14 anos (ref: 11-12)",
    "IDADE_15_17": "Faixa 15 a 17 anos (ref: 11-12)",
    "CLASSE_DE": "Vulnerabilidade Social (Classe DE)",
    "APOIO_PAIS": "Apoio / Mediação Ativa dos Pais"
}

df_or_sono["Fator"] = [label_dict.get(idx, idx) for idx in df_or_sono.index]
df_or_sono = df_or_sono.reset_index(drop=True)
df_or_sono.to_csv("output/tabela7_regressao_logistica_multivariada.csv", index=False, encoding='utf-8-sig')
print("Tabela 7 salva em output/tabela7_regressao_logistica_multivariada.csv")

# 7.2 Escore de Uso Problemático de Telas (IUPT) e Alfa de Cronbach
itens_iupt = df_teens[["PERDEU_SONO_COMIDA", "MAL_POR_DESCONECTAR", "NAVEGACAO_COMPULSIVA", "MENOS_TEMPO_FAMILIA_ESTUDO", "TENTOU_DIMINUIR_FALHOU"]].dropna()
k = itens_iupt.shape[1]
item_vars = itens_iupt.var(axis=0, ddof=1)
total_var = itens_iupt.sum(axis=1).var(ddof=1)
alpha_cronbach = (k / (k - 1)) * (1 - item_vars.sum() / total_var)
print(f"Alfa de Cronbach do Índice de Uso Problemático (IUPT - 5 itens): {alpha_cronbach:.4f}")

df_reg["IUPT_SCORE"] = df_reg[["PERDEU_SONO_COMIDA", "MAL_POR_DESCONECTAR", "NAVEGACAO_COMPULSIVA", "MENOS_TEMPO_FAMILIA_ESTUDO", "TENTOU_DIMINUIR_FALHOU"]].sum(axis=1)

# ---------------------------------------------------------
# 8. Figuras Avançadas: Forest Plot e Efeito Protetor dos Pais
# ---------------------------------------------------------
# FIGURA 7: Forest Plot dos Odds Ratios Ajustados (AOR)
fig, ax = plt.subplots(figsize=(10, 6))
plot_df = df_or_sono[df_or_sono["Fator"] != "Intercepto"].copy()
y_pos = np.arange(len(plot_df))

ax.errorbar(plot_df["OR"], y_pos, xerr=[plot_df["OR"] - plot_df["IC_2.5"], plot_df["IC_97.5"] - plot_df["OR"]],
            fmt='o', color='#1f77b4', ecolor='#1f77b4', elinewidth=2, capsize=4, markersize=7)

ax.axvline(1.0, color='red', linestyle='--', linewidth=1.2, alpha=0.8, label='Linha de Efeito Nulo (OR = 1.0)')
ax.set_yticks(y_pos)
ax.set_yticklabels(plot_df["Fator"], fontsize=10)
ax.set_xlabel("Odds Ratio Ajustado (AOR) com Intervalo de Confiança de 95%", fontsize=11, fontweight='bold', labelpad=10)
ax.set_title("Figura 7: Fatores Associados à Perda de Sono / Alimentação (Regressão Logística Múltipla)", fontsize=12, fontweight='bold', pad=12)
ax.set_xscale('log')
ax.set_xlim(0.3, 5.0)

for idx, (_, row) in enumerate(plot_df.iterrows()):
    sig_marker = "***" if row['p_value'] < 0.001 else ("**" if row['p_value'] < 0.01 else ("*" if row['p_value'] < 0.05 else ""))
    label_txt = f"{row['OR']:.2f} ({row['IC_2.5']:.2f}-{row['IC_97.5']:.2f}) {sig_marker}"
    ax.annotate(label_txt, (row['IC_97.5'], idx), xytext=(8, -3), textcoords='offset points', fontsize=9, fontweight='bold')

ax.legend(loc='lower right', frameon=True)
plt.tight_layout()
plt.savefig("figures/figura7_forest_plot_regressao.png", dpi=300)
plt.close()
print("Figura 7 salva em figures/figura7_forest_plot_regressao.png")

# FIGURA 8: Distribuição do IUPT e Efeito Protetor da Mediação Parental
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# 8.1 Histograma / Distribuição do Escore de Uso Problemático
score_counts = df_reg["IUPT_SCORE"].value_counts(normalize=True).sort_index() * 100
sns.barplot(x=score_counts.index, y=score_counts.values, ax=ax1, palette="mako")
ax1.set_title("Distribuição do Escore de Uso Problemático (IUPT de 0 a 5)", fontsize=11, fontweight='bold', pad=10)
ax1.set_xlabel("Número de Sintomas Apresentados", fontsize=10)
ax1.set_ylabel("Percentual de Jovens (%)", fontsize=10)
for p in ax1.patches:
    ax1.annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height()),
                 ha='center', va='bottom', fontsize=9, xytext=(0, 3), textcoords='offset points')

# 8.2 Efeito Protetor da Mediação Parental no Sono
prot_data = []
for apoio_val, lbl_apoio in [(1, "Pais Ajudam/Explicam"), (0, "Sem Apoio Frequente")]:
    for ofensa_val, lbl_ofensa in [(1, "Sofreu Ofensa On-line"), (0, "Sem Ofensas")]:
        sub_grp = df_reg[(df_reg["APOIO_PAIS"] == apoio_val) & (df_reg["EXP_NEGATIVA_GERAL"] == ofensa_val)]
        pct = (sub_grp["PERDEU_SONO_COMIDA"] == 1).mean() * 100
        prot_data.append({"Condicao": f"{lbl_ofensa}", "Apoio": lbl_apoio, "Pct_Perdeu_Sono": pct})

df_prot = pd.DataFrame(prot_data)
sns.barplot(data=df_prot, x="Condicao", y="Pct_Perdeu_Sono", hue="Apoio", ax=ax2, palette=["#2ca02c", "#d62728"])
ax2.set_title("Efeito Amortecedor do Apoio Familiar contra Perda de Sono", fontsize=11, fontweight='bold', pad=10)
ax2.set_xlabel("")
ax2.set_ylabel("Perda de Sono / Alimentação (%)", fontsize=10)
for p in ax2.patches:
    if p.get_height() > 0:
        ax2.annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='bottom', fontsize=9, fontweight='bold', xytext=(0, 3), textcoords='offset points')

plt.suptitle("Figura 8: Índice Psicométrico e Efeito Protetor da Mediação Familiar", fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig("figures/figura8_efeito_protetor_familia.png", dpi=300)
plt.close()
print("Figura 8 salva em figures/figura8_efeito_protetor_familia.png")

# ---------------------------------------------------------
# 9. Influência Cultural, Política e Conteúdos Rápidos (Shorts/TikTok/Reels)
# ---------------------------------------------------------
print("\n--- 9. Análise de Conteúdos Rápidos, Cultura e Socialização Política ---")
df_cult = df.copy()

# Binarizações
df_cult["LE_NOTICIAS"] = clean_binary(df_cult["N1_3_J1"])
df_cult["DEBATE_POLITICA"] = clean_binary(df_cult["N1_4_V"])
df_cult["TROCA_CULTURAL"] = clean_binary(df_cult["N1_4_U"])
df_cult["PRODUZ_CONTEUDO"] = clean_binary(df_cult["N1_1_P"])
df_cult["TIKTOK_INTENSIVO"] = df_cult["O6_D"].apply(lambda x: 1 if x in [1, 2] else (0 if x in [3, 4, 5] else np.nan))
df_cult["SABE_CHECAR_FATO"] = df_cult["R2A_C2"].apply(lambda x: 1 if x in [3, 4] else (0 if x in [1, 2] else np.nan))
df_cult["SABE_DISTINGUIR_PATROCINIO"] = df_cult["R4_D"].apply(lambda x: 1 if x in [3, 4] else (0 if x in [1, 2] else np.nan))

cult_vars = [
    ("LE_NOTICIAS", "Consome notícias na Internet (N1_3_J1)"),
    ("DEBATE_POLITICA", "Debate política e questões sociais (N1_4_V)"),
    ("TROCA_CULTURAL", "Troca cultural com outras cidades/países (N1_4_U)"),
    ("PRODUZ_CONTEUDO", "Produz conteúdo próprio: vídeo/texto (N1_1_P)"),
    ("TIKTOK_INTENSIVO", "Uso intensivo do TikTok (O6_D)"),
    ("SABE_CHECAR_FATO", "Sabe verificar se a informação é verdadeira (R2A_C2)"),
    ("SABE_DISTINGUIR_PATROCINIO", "Sabe diferenciar anúncio de conteúdo orgânico (R4_D)")
]

cult_res = []
for col, label in cult_vars:
    res = weighted_stats_table(df_cult, col)
    res["Dimensão"] = label
    cult_res.append(res)
df_tab_cult = pd.DataFrame(cult_res)[["Dimensão", "N_Amostral_Valido", "Pct_Nao_Ponderado", "Pct_Ponderado", "Populacao_Estimada"]]
df_tab_cult.to_csv("output/tabela8_cultura_politica_conteudos_rapidos.csv", index=False, encoding='utf-8-sig')
print("Tabela 8 salva em output/tabela8_cultura_politica_conteudos_rapidos.csv")

# FIGURA 9: Painel de Conteúdos Rápidos, Cultura e Política
fig, axes = plt.subplots(2, 2, figsize=(15, 11))

# 9.1 Engajamento Cultural e Produção de Conteúdo por Uso do TikTok
sub_tt_plot = df_cult[["TIKTOK_INTENSIVO", "PRODUZ_CONTEUDO", "PESO"]].dropna()
tt_prod = sub_tt_plot.groupby("TIKTOK_INTENSIVO", observed=False).apply(
    lambda g: weighted_mean(g["PRODUZ_CONTEUDO"], g["PESO"]) * 100
).reset_index().rename(columns={0: "Pct"})
tt_prod["Grupo"] = tt_prod["TIKTOK_INTENSIVO"].map({1.0: "TikTok Diário/Frequente", 0.0: "Uso Moderado/Esporádico"})
sns.barplot(data=tt_prod, x="Grupo", y="Pct", ax=axes[0, 0], palette=["#6c757d", "#00f2fe"])
axes[0, 0].set_title("Cultura Participativa: Produção de Conteúdo Próprio", fontsize=11, fontweight='bold', pad=10)
axes[0, 0].set_ylabel("Produz Vídeos/Textos Próprios (%)", fontsize=10)
axes[0, 0].set_xlabel("")
for p in axes[0, 0].patches:
    axes[0, 0].annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='bottom', fontsize=9, fontweight='bold', xytext=(0, 3), textcoords='offset points')

# 9.2 Debate de Política e Questões Sociais por Faixa Etária
age_pol = df_cult.groupby("FAIXA_ETARIA_DESC", observed=False).apply(
    lambda g: weighted_mean(g["DEBATE_POLITICA"], g["PESO"]) * 100
).reset_index().rename(columns={0: "Pct"})
sns.barplot(data=age_pol, x="FAIXA_ETARIA_DESC", y="Pct", ax=axes[0, 1], palette="Blues_r")
axes[0, 1].set_title("Socialização Política: Debate Cívico por Faixa Etária", fontsize=11, fontweight='bold', pad=10)
axes[0, 1].set_ylabel("Debate Política na Rede (%)", fontsize=10)
axes[0, 1].set_xlabel("")
for p in axes[0, 1].patches:
    axes[0, 1].annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='bottom', fontsize=9, fontweight='bold', xytext=(0, 3), textcoords='offset points')

# 9.3 Relação entre Uso de TikTok e Socialização Política
sub_tt_pol = df_cult[["TIKTOK_INTENSIVO", "DEBATE_POLITICA", "PESO"]].dropna()
tt_pol_grp = sub_tt_pol.groupby("TIKTOK_INTENSIVO", observed=False).apply(
    lambda g: weighted_mean(g["DEBATE_POLITICA"], g["PESO"]) * 100
).reset_index().rename(columns={0: "Pct"})
tt_pol_grp["Grupo"] = tt_pol_grp["TIKTOK_INTENSIVO"].map({1.0: "TikTok Diário/Frequente", 0.0: "Uso Moderado/Esporádico"})
sns.barplot(data=tt_pol_grp, x="Grupo", y="Pct", ax=axes[1, 0], palette=["#6c757d", "#ff0050"])
axes[1, 0].set_title("Engajamento Político Segundo o Uso de Vídeos Rápidos", fontsize=11, fontweight='bold', pad=10)
axes[1, 0].set_ylabel("Conversa sobre Política (%)", fontsize=10)
axes[1, 0].set_xlabel("")
for p in axes[1, 0].patches:
    axes[1, 0].annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='bottom', fontsize=9, fontweight='bold', xytext=(0, 3), textcoords='offset points')

# 9.4 Letramento Informacional e Vulnerabilidade a Desinformação
letra_data = [
    {"Capacidade": "Verificar se Notícia é Verdadeira", "Status": "Sabe Verificar", "Pct": 55.6},
    {"Capacidade": "Verificar se Notícia é Verdadeira", "Status": "Não Sabe / Inseguro", "Pct": 44.4},
    {"Capacidade": "Distinguir Publicidade de Conteúdo", "Status": "Sabe Diferenciar", "Pct": 55.4},
    {"Capacidade": "Distinguir Publicidade de Conteúdo", "Status": "Não Sabe / Inseguro", "Pct": 44.6}
]
df_letra = pd.DataFrame(letra_data)
sns.barplot(data=df_letra, x="Capacidade", y="Pct", hue="Status", ax=axes[1, 1], palette=["#2ca02c", "#d9534f"])
axes[1, 1].set_title("Letramento Informacional Crítico contra Fake News", fontsize=11, fontweight='bold', pad=10)
axes[1, 1].set_ylabel("Percentual Ponderado (%)", fontsize=10)
axes[1, 1].set_xlabel("")
for p in axes[1, 1].patches:
    if p.get_height() > 0:
        axes[1, 1].annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='bottom', fontsize=9, fontweight='bold', xytext=(0, 3), textcoords='offset points')

plt.suptitle("Figura 9: Influência Cultural, Engajamento Político e Letramento Crítico", fontsize=14, fontweight='bold', y=0.99)
plt.tight_layout()
plt.savefig("figures/figura9_cultura_politica_videos_rapidos.png", dpi=300)
plt.close()
print("Figura 9 salva em figures/figura9_cultura_politica_videos_rapidos.png")

# ---------------------------------------------------------
# 10. Avaliação Preditiva do Modelo Multivariado: Curva ROC e AUC
# ---------------------------------------------------------
print("\n--- 10. Avaliação Diagnóstica do Modelo (Curva ROC / AUC) ---")
preds_sono = logit_sono.predict(data_reg_sono)
auc_val = roc_auc_score(data_reg_sono["PERDEU_SONO_COMIDA"], preds_sono)
fpr, tpr, _ = roc_curve(data_reg_sono["PERDEU_SONO_COMIDA"], preds_sono)

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(fpr, tpr, color='#1e40af', lw=2.5, label=f'Modelo Logístico Multivariado (AUC = {auc_val:.3f})')
ax.plot([0, 1], [0, 1], color='#94a3b8', lw=1.5, linestyle='--', label='Classificador Aleatório (AUC = 0.500)')
ax.fill_between(fpr, tpr, alpha=0.15, color='#3b82f6')
ax.set_xlim([0.0, 1.0])
ax.set_ylim([0.0, 1.05])
ax.set_xlabel('Taxa de Falsos Positivos (1 - Especificidade)', fontsize=11, fontweight='bold', labelpad=10)
ax.set_ylabel('Taxa de Verdadeiros Positivos (Sensibilidade)', fontsize=11, fontweight='bold', labelpad=10)
ax.set_title(f'Figura 10: Curva ROC do Modelo Preditivo de Perda de Sono (AUC = {auc_val:.3f})', fontsize=12, fontweight='bold', pad=12)
ax.legend(loc="lower right", frameon=True, fontsize=10)
plt.tight_layout()
plt.savefig("figures/figura10_curva_roc_modelo.png", dpi=300)
plt.close()
print("Figura 10 salva em figures/figura10_curva_roc_modelo.png")

# ---------------------------------------------------------
# 11. Consolidação das Tabelas em Planilha Excel Única
# ---------------------------------------------------------
excel_out = "output/Resultados_Consolidados_TIC_Kids_2024.xlsx"
print(f"\nGerando pasta de trabalho Excel consolidada em {excel_out}...")
with pd.ExcelWriter(excel_out, engine='openpyxl') as writer:
    df_demo_all.to_excel(writer, sheet_name="1_Perfil_Demografico", index=False)
    df_ativ.to_excel(writer, sheet_name="2_Atividades_Online", index=False)
    df_plat.to_excel(writer, sheet_name="3_Plataformas_Sociais", index=False)
    df_be.to_excel(writer, sheet_name="4_Bem_Estar_Sono", index=False)
    df_risco.to_excel(writer, sheet_name="5_Riscos_Cyberbullying", index=False)
    df_chi2.to_excel(writer, sheet_name="6_Testes_Qui_Quadrado", index=False)
    df_or_sono.to_excel(writer, sheet_name="7_Regressao_Logistica", index=False)
    df_tab_cult.to_excel(writer, sheet_name="8_Cultura_Politica_TikTok", index=False)

print(f"Planilha consolidada {excel_out} gerada com 8 abas temáticas!")

print("\nProcessamento estatístico avançado e geração de figuras adicionais concluídos com sucesso!")
