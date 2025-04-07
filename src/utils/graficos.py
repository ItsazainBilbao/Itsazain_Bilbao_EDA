import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append('../')

from utils import edhrec_requests as edh
from utils import funciones
from utils import api_requests as req

flat_colors_distintos = [
        "#E74C3C", "#F39C12", "#2ECC71", "#3498DB", "#9B59B6", "#34495E", 
        "#1ABC9C", "#F1C40F", "#E67E22", "#7F8C8D", "#F5B041", "#D35400", 
        "#16A085", "#27AE60", "#2980B9", "#8E44AD", "#E74C3C", "#D5DBDB", 
        "#8E44AD", "#F39C12", "#3498DB", "#1F618D", "#D45740", "#27AE60", 
        "#DC7633", "#FF6347", "#FFF57F", "#E67E22", "#A3E4D7", "#7D3C98", 
        "#9C27B0", "#FF7F50", "#1A5276", "#16A085", "#F8C471", "#FF9F00", 
        "#D4AC0D", "#2C3E50", "#5DADE2", "#D9E3F0", "#F1C40F", "#E67E22", 
        "#16A085", "#A2D9CE", "#6C3483", "#B9770E", "#D7DBDD", "#F8C471", 
        "#5D6D7E", "#FF6347", "#A569BD", "#F1948A", "#48C9B0", "#27AE60"
    ]

color_map = {
    "W": "#e0ddcfff", "U": "#3B75C4", "B": "#595959ff",
    "R": "#df957aff", "G": "#387771ff", "Incoloro": "#908269db", "Multicolor": "#F2A93B"
}

def dibujar_grafico_uno(df_mazo, titulo = "Grafico uno"):
    df_visu2 = df_mazo.copy()
    # Contamos la cantidad de cartas por 'release_year' y 'set'
    df_yearly_sets = df_visu2.groupby(["release_year", "set"]).size().reset_index(name="count")

    # Crear una columna de 'set_label' para los sets (esto se usará en la leyenda)
    df_yearly_sets["set_label"] = df_yearly_sets["set"]

    # Contamos las ocurrencias de cada 'set' por 'release_year'
    set_counts_per_year = df_yearly_sets.groupby("set_label")["count"].sum()

    # Filtramos los sets que tienen más de 2 cartas en algún año
    sets_mas_de_2_veces = set_counts_per_year[set_counts_per_year > 2].index
   
    # Gráfico de barras con todos los datos
    plt.figure(figsize=(8,6))
    sns.barplot(data=df_yearly_sets, x="release_year", y="count", hue="set_label", dodge=False, palette=flat_colors_distintos)

    plt.xticks(rotation=45)  
    plt.xlabel("Año de Lanzamiento")
    plt.ylabel("Cantidad de Cartas")
    plt.title(titulo)
    plt.grid(axis='y', linestyle="--", alpha=0.7)

    handles, labels = plt.gca().get_legend_handles_labels()
    filtered_handles = []
    filtered_labels = []

    for handle, label in zip(handles, labels):
        if label in sets_mas_de_2_veces:
            filtered_handles.append(handle)
            filtered_labels.append(label)

    plt.legend(filtered_handles, filtered_labels, title="Set", bbox_to_anchor=(1.05, 0.5), loc="center left", ncol=2, frameon=False)
    plt.show()
#Esto es una fumada, para que luego no me funcase con Marina. Este pilla el tipo y te dibuja la línea
#para que puedas comprobar si las cartas publicadas por año del mazo coinciden con la curva de cartas publicadas por tipo específico
def dibujar_grafico_dos(df_mazo, df_cartas, tipo_especifico, titulo ="Gráfico dos"):
    # Crear un dataframe combinado con los sets y tipos por año
    df_mazo_copy = df_mazo.copy()
    df_cartas_copy = df_cartas.copy()

    # Agrupar los datos por año y set para df_mazo
    df_mazo_grouped = df_mazo_copy.groupby(["release_year", "set"]).size().reset_index(name="set_count")
    
    # Filtrar el tipo específico en df_cartas utilizando contains para la columna type_line
    df_cartas_filtered = df_cartas_copy[df_cartas_copy["type_line"].str.contains(tipo_especifico, case=False, na=False)]

    # Agrupar los datos por año y tipo para el tipo específico
    df_cartas_grouped = df_cartas_filtered.groupby(["release_year", "type_line"]).size().reset_index(name="type_count")
    
    #dataframe con todos los años de 1993 a 2025 para el índice
    all_years = pd.DataFrame({'release_year': range(1993, 2026)})

    # Hacer un merge de los dataframes para asegurarse de que todos los años estén presentes
    df_mazo_grouped = pd.merge(all_years, df_mazo_grouped, on="release_year", how="left")
    df_cartas_grouped = pd.merge(all_years, df_cartas_grouped, on="release_year", how="left")

    # Unir ambos dataframes por release_year
    df_combined = pd.merge(df_mazo_grouped, df_cartas_grouped, on="release_year", how="left")

    # Convertir release_year a string para evitar problemas con el eje X
    df_combined["release_year"] = df_combined["release_year"].astype(str)

    # Filtrar los sets que tienen más de 2 cartas en algún año
    # Crear una columna de set_label para los sets para la leyenda
    df_combined["set_label"] = df_combined["set"]
    df_mazo_grouped["set_label"] = df_mazo_grouped["set"]

    # Contamos las cartas de cada set por release_year
    set_counts_per_year = df_mazo_grouped.groupby("set_label")["set_count"].sum()

    # Filtramos los sets que tienen más de 2 cartas en algún año
    sets_mas_de_2_veces = set_counts_per_year[set_counts_per_year > 2].index

  
    fig, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df_combined, x="release_year", y="set_count", hue="set_label", ax=ax1, dodge=False, palette=flat_colors_distintos)

    # Crear el segundo eje para el lineplot de los tipos
    ax2 = ax1.twinx()
    sns.lineplot(data=df_combined, x="release_year", y="type_count", ax=ax2, color='red', marker="o", label=tipo_especifico, linewidth=2, errorbar=None)


    ax1.set_xlabel("Año de Lanzamiento")
    ax1.set_ylabel("Cantidad de Sets")
    ax2.set_ylabel(f"Cantidad de {tipo_especifico}")

    ax1.set_title(titulo)
    handles, labels = ax1.get_legend_handles_labels()
    filtered_handles = []
    filtered_labels = []

    for handle, label in zip(handles, labels):
        if label in sets_mas_de_2_veces:
            filtered_handles.append(handle)
            filtered_labels.append(label)


    ax1.legend(filtered_handles, filtered_labels, title="Sets", loc="upper left", bbox_to_anchor=(1.05, 1), ncol=1)
    ax2.legend(loc="center", bbox_to_anchor=(0.5, 0.95), frameon=True)

    ax1.set_xticks(range(len(df_combined["release_year"].unique())))
    ax1.set_xticklabels(df_combined["release_year"].unique(), rotation=45)

    ax1.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()
