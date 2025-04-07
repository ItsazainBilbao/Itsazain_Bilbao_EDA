import requests
import pandas as pd
from pyedhrec import EDHRec
import os
import numpy as np

##Primera versión
def read_deck_to_dataframe(file_path):
    # Leer el archivo y obtener las líneas
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Extraer el nombre del mazo desde la primera carta (sin la cantidad)
    deck_name = lines[0].split(" ", 1)[1].strip() 

    # Limpiar las líneas y extraer solo el nombre de la carta (sin la cantidad)
    card_names = [line.split(" ", 1)[1].strip() for line in lines]

    # Crear un DataFrame con el nombre del mazo y los nombres de las cartas
    df = pd.DataFrame({
        "Deck Name": [deck_name] * len(card_names),
        "Card Name": card_names
    })

    return df

# Para eliminar los stickers
def load_deck_from_file(file_path):
    all_decks = []  # Lista para almacenar los DataFrames de cada mazo

    # Verificar si el archivo es un archivo .txt
    if file_path.endswith(".txt"): 
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Filtrar líneas en blanco (incluyendo las que tienen solo espacios)
        lines = [line.strip() for line in lines]

        # Buscar el índice del último salto de línea en blanco
        separator_index = None
        for i in range(len(lines) - 1, -1, -1):  
            if lines[i] == "":  
                separator_index = i
                break

        if separator_index is not None and separator_index < len(lines) - 1:
            # Extraer los comandantes desde el final
            commander_lines = lines[separator_index + 1:]
            deck_name = "//".join(commander_lines)  # Formatear con "//"
            card_lines = lines[:separator_index]  # Tomar las cartas hasta el salto de línea
        else:
            print(f"Advertencia: El archivo '{file_path}' no tiene una línea en blanco separando cartas y comandantes. Se omitirá.")
            return None  

        # Aquí vamos a omitir las cartas de STICKERS
        new_card_lines = []
        skip_block = False  # Variable para controlar cuando estamos en el bloque de STICKERS

        for line in card_lines:
            if line.startswith("STICKERS:"):
                skip_block = True  # Empezamos a saltarnos el bloque de STICKERS
                continue
            if skip_block and line == "":  # Si encontramos una línea en blanco después de STICKERS
                skip_block = False  # Deja de saltarse las cartas
                continue
            if not skip_block:
                new_card_lines.append(line)

        # Extraer los nombres de las cartas (evitando los comandantes y las de STICKERS)
        card_names = [line.split(' ', 1)[1] for line in new_card_lines if ' ' in line]

        # Crear DataFrame solo con las cartas que NO sean comandantes ni de STICKERS
        df = pd.DataFrame({
            "Deck Name": [deck_name] * len(card_names),
            "Card Name": card_names
        })

        # Añadir a la lista
        all_decks.append(df)

        # Concatenar todos los DataFrames en uno solo
        if all_decks:
            final_df = pd.concat(all_decks, ignore_index=True)

            # Guardar en CSV para revisión
            # final_df.to_csv("deck.csv", index=False)

            return final_df
        else:
            print(f"No se encontraron cartas en el archivo '{file_path}'.")
            return None
    else:
        print(f"El archivo '{file_path}' no es un archivo .txt válido.")
        return None
    


#Tiene un problema y es que si pilla algo con un nombre parecido, por algún motivo le mete el set que encuentre
#Creo que está arreglado
def añadir_columnas_relevantes(df_Cartas, df_Mazos):
    df_final = df_Mazos.copy()    

    #Antes de nada vamos a eliminar las tierras básicas
    df_final = expolio(df_final)

    # Añadimos columnas vacías para las columnas relevantes
    df_final["type_line"] = np.nan
    df_final["set"] = np.nan
    df_final["released_at"] = np.nan
    df_final["release_year"] = np.nan
    df_final["edhrec_rank"] = np.nan
    df_final["colors"] = np.nan

    # Iteramos sobre cada fila de df_final
    for i, row in df_final.iterrows():
        card_name = row["Card Name"]
        
        # Buscamos los nombres que contengan el de df_final
        match = df_Cartas[df_Cartas["name"].str.contains(fr"\b{card_name}\b", regex=True, na=False, case=False)] #Es por el contains este
        
        # Si encontramos al menos una coincidencia, tomamos la primera
        if not match.empty:
            df_final.at[i, "type_line"] = match.iloc[0]["type_line"]
            df_final.at[i, "set"] = match.iloc[0]["set"]
            df_final.at[i, "released_at"] = match.iloc[0]["released_at"]
            df_final.at[i, "release_year"] = match.iloc[0]["release_year"]
            df_final.at[i, "edhrec_rank"] = match.iloc[0]["edhrec_rank"]
            df_final.at[i, "colors"] = match.iloc[0]["colors"]
    
    df_final["release_year"] = df_final["release_year"].astype("Int64")
    df_final["edhrec_rank"] = df_final["edhrec_rank"].astype("Int64")

    return df_final

#Tercera versión. Ahora es personal.
def load_decks_from_folder3(folder_path):
    all_decks = []  # Lista para almacenar los DataFrames de cada mazo

    # Recorrer todos los archivos en la carpeta
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):  # Solo procesamos archivos .txt
            file_path = os.path.join(folder_path, file_name)

            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            # Filtrar líneas en blanco (incluyendo las que tienen solo espacios)
            lines = [line.strip() for line in lines]

            # Buscar el índice del último salto de línea en blanco
            separator_index = None
            for i in range(len(lines) - 1, -1, -1):  # Recorre las líneas desde el final
                if lines[i] == "":  # Encuentra la última línea vacía real
                    separator_index = i
                    break

            if separator_index is not None and separator_index < len(lines) - 1:
                # Extraer los comandantes desde el final
                commander_lines = lines[separator_index + 1:]
                deck_name = "//".join(commander_lines)  # Formatear con "//"
                card_lines = lines[:separator_index]  # Tomar las cartas hasta el salto de línea
            else:
                print(f"Advertencia: El archivo '{file_name}' no tiene una línea en blanco separando cartas y comandantes. Se omitirá.")
                continue  

            # Aquí vamos a omitir las cartas de STICKERS
            new_card_lines = []
            skip_block = False  # Variable para controlar cuando estamos en el bloque de STICKERS

            for line in card_lines:
                if line.startswith("STICKERS:"):
                    skip_block = True  # Empezamos a saltarnos el bloque de STICKERS
                    continue
                if skip_block and line == "":  # Si encontramos una línea en blanco después de STICKERS
                    skip_block = False  # Deja de saltarse las cartas
                    continue
                if not skip_block:
                    new_card_lines.append(line)

            # Extraer los nombres de las cartas (evitando los comandantes y las de STICKERS)
            card_names = [line.split(' ', 1)[1] for line in new_card_lines if ' ' in line]

            # Crear DataFrame solo con las cartas que NO sean comandantes ni de STICKERS
            df = pd.DataFrame({
                "Deck Name": [deck_name] * len(card_names),
                "Card Name": card_names
            })

            # Añadir a la lista
            all_decks.append(df)

    # Concatenar todos los DataFrames en uno solo
    if all_decks:
        final_df = pd.concat(all_decks, ignore_index=True)
        
        # Guardar en CSV para revisión
        #final_df.to_csv("all_decks.csv", index=False)
        
        return final_df
    else:
        print("No se encontraron archivos de mazos en la carpeta.")
        return None


#FUnción para limpiarme las tierras
def expolio(dataFrame):
    #Aquí expropiamos las tierras normales
    mask = (dataFrame["Card Name"] == "Island") | (dataFrame["Card Name"] == "Forest") | (dataFrame["Card Name"] == "Mountain") | (dataFrame["Card Name"] == "Plains")| (dataFrame["Card Name"] == "Swamp")
    #Aquí expoliamos las tierras nevadas
    maskSnow = (dataFrame["Card Name"] == "Snow-Covered Island") | (dataFrame["Card Name"] == "Snow-Covered Forest") | (dataFrame["Card Name"] == "Snow-Covered Mountain") | (dataFrame["Card Name"] == "Snow-Covered Plains") | (dataFrame["Card Name"] == "Snow-Covered Swamp") 

    dataFrame = dataFrame.drop(dataFrame.loc[mask | maskSnow].index)  

    return dataFrame
#Función que añade la columna de año de publicación
def gestiona_el_Release(dataFrame):
    dataFrame["released_at"] = pd.to_datetime(dataFrame["released_at"], errors="coerce")
    dataFrame["release_year"] = dataFrame["released_at"].dt.year
    return dataFrame