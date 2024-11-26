import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account
import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

@st.cache
def load_data():
   dbm = list(db.collection('movies').stream())
   movies_dict = list(map(lambda x: x.to_dict(), dbm))
   movies = pd.DataFrame(movies_dict)
   return movies

def cargarNombre(titulo):
   filtered_data_byname = dstreamMovies[dstreamMovies['name'].str.contains(titulo,False)]
   return filtered_data_byname

def CargaDirector(director):
    filtered_data_by_director = dstreamMovies[dstreamMovies['director'] == director]
    return filtered_data_by_director

dstreamMovies = load_data()

st.header('Mirame app')

chkAllMovies = st.sidebar.checkbox('Ver todo el catalogo')
if (chkAllMovies):
    dstreamMovies = load_data()

tituloTxt = st.sidebar.text_input('Pelicula:')
buscarBtn = st.sidebar.button('Buscar')

if (buscarBtn):
    dstreamMovies = cargarNombre(tituloTxt)
    conta = dstreamMovies.shape[0]
    st.write(f"Total: {conta}")

lista = st.sidebar.selectbox('Seleccionar Director: ', dstreamMovies['director'].unique())
directorBtn = st.sidebar.button('Filtrar')

if (directorBtn):
    dstreamMovies = CargaDirector(lista)
    conta = dstreamMovies.shape[0]
    st.write(f"Total : {conta}")


st.sidebar.subheader('Nuevo')
nueva = st.sidebar.text_input('Name:')
compania = st.sidebar.selectbox('Company', dstreamMovies['company'].unique())
director = st.sidebar.selectbox('Director', dstreamMovies['director'].unique())
genero = st.sidebar.selectbox('Genre', dstreamMovies['genre'].unique())
nuevoBtn = st.sidebar.button("Crear nuevo filme")

if nueva and compania and director and genero and nuevoBtn:
    doc_ref = db.collection('movies').document().set({
    "name": nueva,
    "company": compania,
    "director": director,
    "genre": genero      
    })
    st.sidebar.write("Registro ingresado")

st.dataframe (dstreamMovies)