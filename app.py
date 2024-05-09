import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

def load_data(csv_file):
    # Carrega o arquivo CSV
    data = pd.read_csv(csv_file)
    return data

def remove_accents(text):
    # Verifica se o valor é uma string antes de tentar remover os acentos
    if isinstance(text, str):
        # Dicionário de mapeamento de caracteres com acentos para caracteres sem acentos
        accent_map = {
            'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a',
            'é': 'e', 'ê': 'e', 'í': 'i', 'ó': 'o',
            'ô': 'o', 'õ': 'o', 'ú': 'u', 'ü': 'u',
            'ç': 'c',
            'Á': 'A', 'À': 'A', 'Ã': 'A', 'Â': 'A',
            'É': 'E', 'Ê': 'E', 'Í': 'I', 'Ó': 'O',
            'Ô': 'O', 'Õ': 'O', 'Ú': 'U', 'Ü': 'U',
            'Ç': 'C'
        }
        # Substitui caracteres acentuados pelos equivalentes sem acentos
        return ''.join(accent_map.get(char, char) for char in text)
    else:
        return text

def display_image_info(data, image_folder):
    
    # Configura o layout para ter 3 imagens por linha
    col1, col2, col3 = st.columns(3)

    # Variable to track the column to use
    current_col = col1

    for index, row in data.iterrows():
        image_path = os.path.join(image_folder, row['Nome do Arquivo']+'.jpg')
        with current_col:
            if(row['URL do post']) =="https://www.instagram.com/p/":
                st.image(image_path, use_column_width=True, caption=f"{row['URL do post']}", width=500)
            else:
                st.image(image_path, use_column_width=True, caption="storie", width=500)
            st.write(f"Possível Raça: {row['Possivel raça']}")
            st.write(f"Cor Aproximada: {row['Cor aproximada']}")
            st.write(f"Porte Aproximado: {row['Porte aproximado']}")
            st.write(f"Peso Aproximado: {row['Peso Aproximado']}")
            st.write(f"Texto do Post: {row['Texto do post']}")
            st.write(f"Texto da imagem: {row['Texto da imagem']}")
            st.markdown("---")
        
        # Switch to the next column
        if current_col == col1:
            current_col = col2
        elif current_col == col2:
            current_col = col3
        else:
            current_col = col1


def main():
    st.title("Pet finder")

    
    selected_csv = st.sidebar.radio("Selecione o CSV:", ['acheseupetrs.csv', 'meubichotasalvocanoas.csv', 'tosalvocanoas.csv'])
    
    csv_folder = './'
    image_folder = selected_csv.split('.')[0]  
    csv_file = os.path.join(csv_folder, selected_csv)
    image_folder = os.path.join('./', image_folder)
    csv_name = selected_csv.replace('.csv','')
    st.header(f"Página instagram {csv_name}")
    
    data = load_data(csv_file)
    
    search_term = st.sidebar.text_input("Buscar por palavra-chave:")
    if search_term:
        
        search_term = remove_accents(search_term)
        
        data_text_cols = data.select_dtypes(include=['object']).columns.drop('Nome do Arquivo')
        data[data_text_cols] = data[data_text_cols].applymap(remove_accents)
        
        data = data[data[data_text_cols].apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)]

    
    
    display_image_info(data, image_folder)

if __name__ == "__main__":
    main()
