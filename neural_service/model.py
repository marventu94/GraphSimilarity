import torch
from pykeen.triples import TriplesFactory
import pandas as pd
import numpy as np

# Declaración de variables globales
model = None
triples_factory = None
data_frame = None

# Función para cargar el modelo y la fábrica de triples al inicio
def initialization_model():
    global model, triples_factory
    # Carga el modelo
    model = torch.load('models/inmuebles_grupo_02/trained_model.pkl')
    
    # Carga el TriplesFactory
    triples_file = 'dataset/dataset_validation.tsv.gz'
    triples_factory = TriplesFactory.from_path(triples_file, create_inverse_triples=True)

    # A partir de la triplefactory creo dos input
    data_frame = pd.read_csv(triples_file, sep='\t', header=None, names=['head', 'relation', 'tail'])

    return model, triples_factory, data_frame

def predict_similarity(inputs):
    heads = _findHeadOnDataFrame(inputs[0])
    tails = _findHeadOnDataFrame(inputs[1])

    heads_idx = [triples_factory.entity_to_id[head] for head in heads]
    tails_idx = [triples_factory.entity_to_id[head] for head in tails]

    relation_idx = [triples_factory.relation_to_id['http://www.w3.org/2002/07/owl#sameAs']] * len(heads_idx)

    hr_batch = torch.tensor(list(zip(heads_idx, relation_idx)))

    scores = model.score_t(hr_batch)

    # Pasa el tensor al modelo para obtener la score
    scores = model.score_t(hr_batch)

    # Calcular el score promedio para todos los tails
    scores_for_tails = [scores[0, tail_idx] for tail_idx in tails_idx]

    # Calcular el promedio de los scores
    average_score = torch.mean(torch.tensor(scores_for_tails)).item()

    # Imprimir el score promedio
    print(f"El score promedio por 'sameAs' es: {average_score}")

    # Definir un umbral para decidir si se cumple la condición
    threshold = -2.0  # Ajusta este valor según tus necesidades

    # Tomar la decisión basada en el score promedio
    if average_score < threshold:
        message = "Los atributos cumplen con la condición 'sameAs'."
    else:
        message = "Los atributos NO cumplen con la condición 'sameAs'."

    probabilidad = 1 / (1 + np.exp(-average_score))

    return {"probabilidad": probabilidad, "description" : message}


def _findHeadOnDataFrame(properties):
    heads_filtrados = set(data_frame['head'])  # Inicializar con todos los heads posibles
    for prop in properties:
        
        relation = prop[0].strip() 
        tail_value = prop[1].strip()

        # Filtrar el DataFrame
        heads_filtrados_prop = data_frame[
            (data_frame['relation'] == relation) & (data_frame['tail'].astype(str) == tail_value)
        ]['head'].unique()

        heads_filtrados = heads_filtrados.intersection(heads_filtrados_prop)
        
    return heads_filtrados