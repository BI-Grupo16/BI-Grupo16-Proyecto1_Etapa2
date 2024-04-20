
import nltk
import os
import joblib
from num2words import num2words
import pandas as pd
# librería Natural Language Toolkit, usada para trabajar con textos
import nltk

# Punkt permite separar un texto en frases.
nltk.download('punkt')

# Descarga de paquete WordNetLemmatizer, este es usado para encontrar el lema de cada palabra
nltk.download('wordnet')

# Descarga todas las palabras vacias, es decir, aquellas que no aportan nada al significado del texto
nltk.download('stopwords')


from sklearn.pipeline import Pipeline


from sklearn.base import TransformerMixin, BaseEstimator

from nltk import word_tokenize

import re
import unicodedata


from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer


class CustomPreprocessor(TransformerMixin, BaseEstimator):
   def __init__(self, tfidf=None):
      self.palabras_a_eliminar = ["h","aqui","viajero","ano","dos","tener","familia","alimento","altura","adulto","comer","torre","calle","general","gente","vistas",'museo','parte','visitar','visita','viaje','vista','playa','restaurantes','personas','historia','siempre','gran','piscina','zona','cada','ser','hacer','aunque','puede','bastante','tan','cuba','alli','ubicacion','agradable','atencion','estan','tenia','agua','recepcion','desayuno','mas','dia','habana','habitaciones','ir','personal','hotel', 'lugar','si','tambien','mejor','restaurante','habitacion','habit','ver','comida','solo','servicio','ciudad','habia','tiempo','noche','despues','asi']
      self.tfidf = tfidf
   
   def fit(self, X, y=None):
      # No se necesita entrenamiento, solo devolver self
      return self

   def transform(self, X):
      # Asegúrate de que X sea una Serie o DataFrame de pandas para aplicar estas operaciones
      X_transformed = X.copy()
      #print(X_transformed)
      # Tokenizar
      X_transformed = X_transformed.apply(word_tokenize)
      #print(X_transformed)
      # Preprocesamiento textos
      X_transformed = X_transformed.apply(self.preprocessing)
      # Aplicar procesamientos
      X_transformed = X_transformed.apply(self.eliminar_risas)
      X_transformed = X_transformed.apply(self.eliminar_palabras)
      X_transformed = X_transformed.apply(self.stem_and_lemmatize)
      # vectorización
      X_transformed = X_transformed.astype('string')
      X_transformed = self.tfidf.transform(X_transformed)
      
      return X_transformed
   
      
   # Función para eliminar las palabras de una lista
   def eliminar_palabras(self, lista):
      return [palabra for palabra in lista if palabra not in self.palabras_a_eliminar]

   def eliminar_risas(self, lista):
      words = []
      for word in lista:
            if not('jaj' in word) or not('hah' in word):
               words.append(word)
      return words

   def stem_words(self, words):
      """Stem words in list of tokenized words"""
      sbs = SnowballStemmer(language="spanish")
      new_words = []
      for word in words:
            new_word = sbs.stem(word)
            new_words.append(new_word)
      return new_words

   def lemmatize_verbs(self, words):
      """Lemmatize verbs in text (Spanish)"""
      nlp = spacy.load("es_core_news_sm")
      text = join_words(words)
      doc = nlp(text)
      lemmas = [token.lemma_ if token.pos_ == "VERB" else token.text for token in doc]
      return lemmas

   def stem_and_lemmatize(self, words):
      stems = self.stem_words(words)
      #lemmas = lemmatize_verbs(words)
      #return lemmas
      return stems

   def remove_non_ascii(self, words):
      """Remove non-ASCII characters from list of tokenized words"""
      new_words = []
      for word in words:
            if word is not None:
               new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
               new_words.append(new_word)
      return new_words

   def to_lowercase(self, words):
      """Convert all characters to lowercase from list of tokenized words"""
      return [x.lower() for x in words]


   def remove_punctuation(self, words):
      """Remove punctuation from list of tokenized words"""
      new_words = []
      for word in words:
            if word is not None:
               new_word = re.sub(r'[^\w\s]', '', word)
               if new_word != '':
                  new_words.append(new_word)
      return new_words


   def replace_numbers(self, words):
      """Replace all integer occurrences in list of tokenized words with textual representation in Spanish"""
      new_words = []
      for word in words:
            if word.isdigit():
               new_word = num2words(int(word), lang='es')
               new_words.append(new_word)
            else:
               new_words.append(word)
      return new_words

   def remove_stopwords(self, words):
      """Remove stop words from list of tokenized words"""
      stop_words = set(stopwords.words('spanish'))
      filtered_sentence = []

      for w in words:
            if w not in stop_words:
               filtered_sentence.append(w)
      return filtered_sentence

   def remove_non_alphanumeric(self, words):
      return [re.sub(r'[^\w\s]', '', item) for item in words]

   def preprocessing(self, words):
      words = self.to_lowercase(words)
      words = self.replace_numbers(words)
      words = self.remove_punctuation(words)
      words = self.remove_non_ascii(words)
      words = self.remove_stopwords(words)
      return words


def create_pipeline():
    tfidf = joblib.load(os.path.join('assets','tfidf.joblib')) ###
    
    pipeline = Pipeline([
        ('preprocessor', CustomPreprocessor(tfidf)),
        ('classifier', joblib.load(os.path.join('assets','modelo_regresion.joblib')))
    ])

    return pipeline

