import numpy as np
import pandas as pd
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import googletrans
from googletrans import Translator
import random
from sklearn.cluster import AgglomerativeClustering
import scipy.cluster.hierarchy as sch
import json
import pickle

alfabeto = {
    "a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h" : 7,
    "i" : 8, "j" : 9, "k" : 10, "l" : 11, "m" : 12, "n" : 13, "ñ" : 14, "o" : 15,
    "p" : 16, "q" : 17, "r" : 18, "s" : 19, "t" : 20, "u" : 21, "v" : 22, "w" : 23,
    "x" : 24, "y" : 25, "z" : 26, " ": 27 
}

num2char = list(alfabeto.keys())

#funciones

#elimina símbolos como tildes y si esta en mayuscula
def reduce_frase(frase):
    fraseToReduce = frase.lower()
    fraseToReduce = fraseToReduce.replace('.', '')
    fraseToReduce = fraseToReduce.replace(',', '')
    fraseToReduce = fraseToReduce.replace(':', '')
    fraseToReduce = fraseToReduce.replace('!', '')
    fraseToReduce = fraseToReduce.replace("©", "") 
    fraseToReduce = fraseToReduce.replace('á', 'a')
    fraseToReduce = fraseToReduce.replace("\n", "")
    fraseToReduce = fraseToReduce.replace("“", "")
    fraseToReduce = fraseToReduce.replace("”", "")
    fraseToReduce = fraseToReduce.replace("?", "")
    fraseToReduce = fraseToReduce.replace('"', "")
    fraseToReduce = fraseToReduce.replace("¿", "")
    fraseToReduce = fraseToReduce.replace("¡", "")
    fraseToReduce = fraseToReduce.replace(";", "")
    fraseToReduce = fraseToReduce.replace("«","")
    fraseToReduce = fraseToReduce.replace("»", "")
    fraseToReduce = fraseToReduce.replace("…","")
    fraseToReduce = fraseToReduce.replace("-","")
    fraseToReduce = fraseToReduce.replace("(","")
    fraseToReduce = fraseToReduce.replace(")","")
    fraseToReduce = fraseToReduce.replace("/","")
    fraseToReduce = fraseToReduce.replace("ó", "o")
    fraseToReduce = fraseToReduce.replace('é', 'e')
    fraseToReduce = fraseToReduce.replace('ú', 'u')
    fraseToReduce = fraseToReduce.replace('ü', 'u')
    fraseToReduce = fraseToReduce.replace('í', 'u')
    return fraseToReduce


def num_tranform (frase):
    return [alfabeto[l] for l in frase ]

def num2char_transform (phase_num_trans):
    return "".join([num2char[e] for e in phase_num_trans])

def encode_cesar(array, traslation):
    array_num = np.asarray(array)
    array_num += traslation
    array_num %= 28
    return list(array_num)


def encoder_frase(frase):
    numero = random.randint(-28,28)
    frase = reduce_frase(frase)
    frase = num_tranform(frase)
    frase = encode_cesar(frase, numero)
    return frase

def scrapping():

    #the url

    url = "https://psicologiaymente.com/cultura/mejores-poemas-cortos"

    #conectado a el URL

    r = response = requests.get(url).text
    soup = BeautifulSoup(r, "lxml")
    frases = soup.findAll('p')

    frases_obtained = []

    for i in range(0, len(frases)):
        frases[i] = frases[i].get_text()
        frases[i] = reduce_frase(frases[i])
        frases[i] = ''.join([j for j in frases[i] if not j.isdigit()])
        frases[i] = re.sub(r'^"|"$', '', frases[i])
        frases_obtained.append(frases[i])

    return frases_obtained

def tranform_palabras(frase):
    frase_dict = dict.fromkeys(alfabeto.keys(), 0)
    fra = reduce_frase(frase)
    for l in fra:
        frase_dict[l] += 1 
    return frase_dict

#decode con google traslate

def decode_frase_unknown(frase):
    translator = Translator()
    frase = reduce_frase(frase)
    frase = num_tranform(frase)

    for i in range(-29,29):
        frase = encode_cesar(frase, i)
        frase_letra = num2char_transform(frase)
        if(translator.translate(frase_letra).src == 'es'):
            return frase_letra

#decode Fuerza bruta

def decode_frase_unknown_fuerzaBruta(frase):
    frase = reduce_frase(frase)
    frase = num_tranform(frase)

    frases_posibles = []

    for i in range(-29,29):
        frase_traslate = encode_cesar(frase, i)
        frase_letra = num2char_transform(frase_traslate)
        frases_posibles.append(frase_letra)
    
    return frases_posibles

##decode con machine learning

def clasific_ml(x_data):

    with open("pickle_model.pkl", 'rb') as file:
        pickle_model = pickle.load(file)
    
      

    x_data = x_data.reshape(1, -1)
    
    prediction = pickle_model.predict(x_data)

    return prediction


    
def decode_frase_unknown_ml(frase):
    frase = reduce_frase(frase)
    frase = num_tranform(frase)    
    data_param = json.load(open('data.json', 'r'))

    respuesta_posibles = []

    for i in range(-29,29):
        frase_traslate = encode_cesar(frase, i)
        frase_traslate = num2char_transform(frase_traslate)
        data_frase = tranform_palabras(frase_traslate)
        df_frase = np.asarray(list(data_frase.values()))[0:27]
        maximo = np.asarray(data_param["x_max"])
        minimo = np.asarray(data_param["x_min"])
        x_data = (df_frase - minimo)/(maximo - minimo)

        cla = clasific_ml(x_data)

        if cla == 1 :
            respuesta_posibles.append(frase_traslate)    

        frase_traslate = None
        
    return respuesta_posibles



