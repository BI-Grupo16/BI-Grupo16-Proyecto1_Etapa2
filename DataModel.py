from pydantic import BaseModel
from typing import List

class DataModel(BaseModel):

# Estas varibles permiten que la librería pydantic haga el parseo entre el Json recibido y el modelo declarado.
    #year: float
    #km_driven: float
    reviewText: str

#Esta función retorna los nombres de las columnas correspondientes con el modelo esxportado en joblib.
    def columns(self):
        return ["reviewText"]
