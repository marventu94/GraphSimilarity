import torch
from pykeen.triples import TriplesFactory
import pandas as pd
import numpy as np
import os

# Declaración de variables globales
model = None
triples_factory = None
heads = None
heads_idx = None
relation_same_as = None
relation_same_as_idx = None

# Función para cargar el modelo y la fábrica de triples al inicio
def initialization_model():
    global model, triples_factory, heads, heads_idx, relation_same_as, relation_same_as_idx
    # Carga el modelo
    model = torch.load('model/transH_model.pkl', weights_only=False)
    
    # Carga el TriplesFactory
    triples_file = 'model/dataset.tsv.gz'
    triples_factory = TriplesFactory.from_path(triples_file, create_inverse_triples=True)

    # Cargo el DataFrame
    data_frame = pd.read_csv(triples_file, sep='\t', header=None, names=['head', 'relation', 'tail'])

    # Genero los heads & heads_idx y RelationSamesAs & RelationSamesAsIdx
    heads = data_frame[list(map(lambda x: True if ('pronto.owl#space_site' in x) and (len(x.split('#')[1].split('_')) == 3) else False, data_frame['head'].values))]['head'].values
    heads_idx = [triples_factory.entity_to_id[head] for head in heads]

    relation_same_as = 'http://www.w3.org/2002/07/owl#sameAs'
    relation_same_as_idx = triples_factory.relation_to_id[relation_same_as]

    return model, triples_factory, heads, heads_idx, relation_same_as, relation_same_as_idx

def predict_similarity(entity_input):
    result = __validate_input(entity_input)
    scores = model.score_t(torch.tensor([[result, 5]]))
    top_10_values, top_10_indices = torch.topk(scores, k=scores.size(1), dim=1, largest=False)
    similarity_entities = __get_top_entities(top_10_values, top_10_indices)
    return similarity_entities

def __get_top_entities(top_10_values, top_10_indices):
    entities_with_scores = []
    for row_indices, row_scores in zip(top_10_indices, top_10_values):
        for index, score in zip(row_indices, row_scores):
            head_id = __safe_get(index.item())
            if head_id is not None:
                entity = triples_factory.entity_id_to_label.get(head_id)
                entities_with_scores.append((entity, score.item()))
            if len(entities_with_scores) == 10:
                return entities_with_scores
    return entities_with_scores

def __safe_get(index):
    try:
        return heads_idx[index]
    except IndexError:
        return None
    
def __validate_input(entity_input):
    # Si es un ID, verificar que está en heads_idx
    if isinstance(entity_input, int):
        if entity_input in heads_idx:
            return entity_input
        raise ValueError(f"El ID '{entity_input}' no está en los heads permitidos (heads_idx).")

    # Si es un string, intentar convertirlo a un ID con triples_factory
    if isinstance(entity_input, str):
        try:
            entity_id = triples_factory.entity_to_id[entity_input]
            if entity_id in heads_idx:
                return entity_id
            raise ValueError(f"El head '{entity_input}' (ID {entity_id}) no está en los heads permitidos (heads_idx).")
        except KeyError:
            raise ValueError(f"El head '{entity_input}' no existe en la TriplesFactory.")

    # Si el input no es válido, lanzar una excepción
    raise TypeError("El input debe ser un string (head) o un entero (id).")