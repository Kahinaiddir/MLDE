# Guide de l'utilisateur
--- 

# Déploiement d'un modèle de prévision des incendies de forêt

Ce document décrit les étapes nécessaires au déploiement d'un modèle d'apprentissage automatique
entraîné pour prédire la gravité des incendies de forêt. Le modèle est suivi et sauvegardé avec MLflow, et nous
utiliserons FastAPI pour le servir en tant qu'API.

## Table des matières

```
1.Description de l'ensemble de données
2.Formation et enregistrement des modèles
3.Déploiement du modèle
4.Test de l'API
```
## Description de l'ensemble de données

Le jeu de données utilisé dans ce projet est conçu pour prédire la zone touchée par les incendies de forêt
dans la région nord-est du Portugal. Il comprend les caractéristiques suivantes :

```
Variables spatiales : X , Y- Coordonnées à l'intérieur du parc de Montesinho.

Variables temporelles : mois , jour - - Mois et jour de la semaine où les données ont été enregistrées.

Variables météorologiques :
        FFMC (Fine Fuel Moisture Code)   / (Code d'humidité du  combustible fin)
        DMC (Duff Moisture Code)  /  (Code d'humidité du Duff)
        DC (Drought Code) /  (Code de sécheresse)
        ISI (Initial Spread Index) /(Indice d'écart initial)

Conditions météorologiques :
temp - Température en Celsius.
RH - Humidité relative (%).
wind - Vitesse du vent (km/h).
rain- Pluies (mm).

Variable cible : zone - La superficie brûlée en hectares.

```
Ces variables sont prétraitées et mises à l'échelle dans le cadre du processus de formation afin de garantir
que toutes les entrées sont à une échelle comparable.

## Formation et enregistrement des modèles

```
1.Prétraitement des données :
Chargez l'ensemble de données et vérifiez qu'il n'y a pas de valeurs manquantes.
Mettre à l'échelle les caractéristiques à l'aide de StandardScaler.

2.Séparation de la formation et de l'essai :
Divisez les données en 80-20 pour la formation et le test.

3.Définition du modèle :
Définir un modèle de réseau neuronal à l'aide de Keras , avec une architecture adaptée à la
régression (par exemple, des couches denses avec activation ReLU).
Compiler le modèle avec l'optimiseur ( adam ), la fonction de perte (mean_squared_error ) et les métriques appropriés.

4.Former le modèle :
Entraîner validation le modèle sur l'ensemble d'apprentissage, en enregistrant les pertes d'apprentissage et de validation.

5.Évaluer et enregistrer le modèle :
Calculer les mesures de performance, telles que MSE et R².
Enregistrer le modèle et les métriques avec MLflow pour le suivi et la gestion des versions.
 Voici un exemple de journalisation avec MLflow :

import mlflow import
mlflow.keras
from mlflow.models.signature import infer_signature
import numpy as np

with mlflow.start_run() : mlflow.log_param("n_features",
X_train.shape[1]) mlflow.log_param("epochs", 100 )
mlflow.log_param("batch_size", 32)

# Log des métriques
mlflow.log_metric("mse", mse)
mlflow.log_metric("r2", r2)

# Modèle d'enregistrement avec signature pour la validation des entrées
signature = infer_signature(X_train, model.predict(X_train)) mlflow.keras.log_model(
model,
artifact_path="forest_fire_prediction_model",
signature=signature, input_example=X_train[: 1 ],
registered_model_name="tracking_forest_fire_prediction_model"
)

6.Sauvegarder le modèle pour le déploiement :
Une fois formé et enregistré, le modèle est sauvegardé en tant qu'artefact MLflow et une version unique lui est attribuée dans le registre des modèles MLflow.

# MLflow

```
MLflow est une plateforme open-source qui aide à gérer le cycle de vie de l'apprentissage
automatique. Elle fournit des outils pour le suivi des expériences, montre comment enregistrer les expériences, les paramètres et les métriques, pendant le développement du modèle, l'emballage des modèles et leur déploiement en production.
```

```
Voici un lien vers la documentation MLflow : https://mlflow.org/docs/latest/index.html
```
# Suivi des expériences :

```
MLflow enregistre les données utilisées, le code exécuté et les performances de chaque tentative (modèle). Il est ainsi facile de suivre les progrès réalisés, de comparer différents modèles et d'apprendre de nos erreurs.
```
Paramètres de journalisation et mesures :

MLflow nous permet d'enregistrer à la fois les paramètres et les métriques afin que nous puissions voir comment la modification des paramètres affecte les résultats finaux. Cela nous permet d'affiner notre modèle et de le rendre encore meilleur.




## Déploiement du modèle

### Étape 1 : Installation des dépendances
Assurez-vous que FastAPI et Uvicorn sont installés :
```
pip install fastapi uvicorn
```

### Étape 2 : Créer le code de déploiement FastAPI
Exécutez un fichier Python (par exemple, main.py ) avec le code suivant pour déployer le modèle en tant qu'API à l'aide de FastAPI. Ce code servira le modèle en tant qu'API, en acceptant les demandes au format JSON et en renvoyant les prédictions.
```
from fastapi import FastAPI, HTTPException from
pydantic import BaseModel
import mlflow import
pandas as pd
# Chargement du modèle à partir de MLflow
MODEL_URI = "models:/tracking_forest_fire_prediction_model/latest" model =
mlflow.pyfunc.load_model(MODEL_URI)
app = FastAPI()
# Définir le schéma de la demande
classe PredictionRequest(BaseModel) : X :
float
Y : float
month : float
day : float
FFMC : float
DMC : float
DC : float
ISI : float
temp : float
RH : float
vent : float
pluie :
float
classe PredictionResponse(BaseModel) : prediction :
float
@app.get("/") def
read_root() :
returnde prédiction {"message" des :incendies "Welcome de to for theêt) Forest Fire Prediction API"} (Bienvenue dans l'API ) 

@app.post("/predict", response_model=PredictionResponse) def
predict(data : PredictionRequest) :
essayer :
# Convertir les données d'entrée en DataFrame
input_data = pd.DataFrame([data.dict()]) #
Générer la prédiction
prediction = model.predict(input_data)
return PredictionResponse(prediction=prediction[ 0 ][ 0 ]) # En supposant une seule
sortie
sauf Exception comme e :
raise HTTPException(status_code=500, detail=f "Erreur de prédiction :
{str(e)}")
```




# Déploiement :

Le déploiement consiste à mettre notre modèle sur le marché.

## Étape 3 : Exécuter l'application FastAPI

Exécuter l'API à l'aide d'Uvicorn :
```
uvicorn main:app --host 0 .0.0.0 --port 8000 - -reload
```

L'API sera désormais disponible à l'adresse [http://localhost:](http://localhost:).
```
http://localhost:8000/predict
```




## Test de l'API

### Étape 1 : Faire une demande de prédiction

Envoyez une requête POST avec des données JSON comme suit :
{
"X" : - 0. 5 ,
"Y" : - 0. 2 ,
"mois" : 0. 5 ,
"jour" : - 0. 1 ,
"FFMC" : 0. 4 ,
"DMC" : - 0. 5 ,
"DC" : - 0. 3 ,
"ISI" : - 0. 3 ,
"temp" : 0. 1 ,
"RH" : - 0. 5 ,
"vent" : - 0. 5 ,
"pluie" : - 0. 1
}
```

### Étape 2 : Vérifier la réponse

La réponse sera au format JSON avec la valeur prédite, par exemple :
```
{
"prédiction" : 0.1234
}
```

### Notes clés

```
1.Versionnement du modèle : En utilisant MLflow, nous pouvons récupérer la dernière version du modèle automatiquement avec
```
MODEL_URI = "models:/tracking_forest_fire_prediction_model/latest".
```
2.Évolutivité : Cette API peut être déployée sur des services en nuage comme AWS ou Google Cloud pour une meilleure évolutivité.
3.Gestion des erreurs : L'application FastAPI comprend une gestion des erreurs de prédiction à l'aide de la fonction :
```
HTTPException.
```

### Informations complémentaires

```
Intégration de MLflow : MLflow permet de suivre les métriques et les paramètres du modèle, ce qui est particulièrement utile pour l'amélioration continue du modèle.
Registre des modèles : Le registre de modèles de MLflow permet de garder une trace des différentes versions du modèle, ce qui est utile en production lorsque le dernier modèle doit être déployé fréquemment.
Documentation API : FastAPI génère automatiquement une documentation interactive sur l'API, disponible à l'adresse http://localhost:8000/docs.
```

