from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Importar el middleware CORS

from DataModel import DataModel
from joblib import load
from fastapi.responses import HTMLResponse

import os
import pandas as pd

from pipeline import create_pipeline

app = FastAPI()
pipeline = create_pipeline()

# Definir la configuración de CORS
origins = ["*"]  # Esto permite solicitudes desde cualquier origen. Puedes especificar los orígenes permitidos según tus necesidades.

# Agregar el middleware CORS a la aplicación
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Puedes especificar los métodos HTTP permitidos
    allow_headers=["*"],  # Puedes especificar los encabezados permitidos
)

@app.get("/", response_class=HTMLResponse)
async def read_items():
   html_path = os.path.join('templates', 'index.html')
   with open(html_path, 'r') as file:  # r to open file in READ mode
      html_content = file.read()

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
   df = pd.DataFrame({'Review': [dataModel.reviewText]})

   # Hacer predicciones con el pipeline cargado
   predictions = pipeline.predict(df['Review'])

   probabilities = pipeline.predict_proba(df['Review'])

   # Convertir las predicciones y probabilidades a lista para enviar como JSON
   return {
      "predictions": predictions.tolist(),
      "probabilities": probabilities.tolist()  # Asume que quieres todas las probabilidades
   }
