from typing import Optional

from fastapi import FastAPI

from DataModel import DataModel

from joblib import load

from fastapi.responses import HTMLResponse

import os
import pandas as pd

from pipeline import create_pipeline

app = FastAPI()
pipeline = create_pipeline()

#data = {'Review': ['PESIMO', 'aaaa']}
#df = pd.DataFrame(data)
#a = pipeline.predict(df['Review'])
#print(a)


@app.get("/", response_class=HTMLResponse)
async def read_items():
   html_path = os.path.join('templates', 'index.html')
   with open(html_path, 'r') as file:  # r to open file in READ mode
      html_content = file.read()


   # crear dataframe con columna REview
   

   return HTMLResponse(content=html_content, status_code=200)


@app.get("/")
def read_root():
   return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
   return {"item_id": item_id, "q": q}


# ARCHIVO
@app.post("/predictions")
def make_predictions(dataModel: DataModel):
   df = pd.DataFrame(dataModel.dict(), columns=dataModel.dict().keys(), index=[0])
   df.columns = dataModel.columns()
   pipeline = load("assets/pipeline.joblib")
   # pipeline ()
   result = model.predict(df)
   return result

# INDIVIDUAL
@app.post("/prediction")
def make_prediction(dataModel: DataModel):
   #print(dataModel.reviewText)
   df = pd.DataFrame({'Review': [dataModel.reviewText]})

   # Hacer predicciones con el pipeline cargado
   predictions = pipeline.predict(df['Review'])

   probabilities = pipeline.predict_proba(df['Review'])

   # Convertir las predicciones y probabilidades a lista para enviar como JSON
   return {
      "predictions": predictions.tolist(),
      "probabilities": probabilities.tolist()  # Asume que quieres todas las probabilidades
   }