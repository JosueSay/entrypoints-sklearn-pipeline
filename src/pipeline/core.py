"""Carga de datos y construccion del Pipeline desde los entrypoints."""
import sys

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points

GRUPO_PASOS = "pipeline.steps"


def obtener_datos(file_id="10S8JVFiLfCoRB9mb0NJG5YhITyXbH37B"):
    """Descarga el CSV de clientes de tarjeta de credito."""
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    return pd.read_csv(url)


def filtrar_datos(data):
    """Quita las columnas de identificador."""
    return data.drop(columns=["Sl_No", "Customer Key"])


def separar_datos(X):
    """Divide en entrenamiento, validacion y prueba (60/20/20)."""
    X_train_val, X_test = train_test_split(X, test_size=0.20, random_state=42)
    X_train, X_val = train_test_split(X_train_val, test_size=0.25, random_state=42)
    return X_train, X_val, X_test


def descubrir_pasos(grupo=GRUPO_PASOS):
    """Devuelve los pasos registrados en el grupo, ordenados por nombre.

    El grupo no garantiza un orden de lectura y en un Pipeline el orden es
    parte del resultado, por eso los nombres llevan prefijo numerico.
    """
    encontrados = entry_points(group=grupo)
    return [ep.load()() for ep in sorted(encontrados, key=lambda ep: ep.name)]


def crear_pipeline(grupo=GRUPO_PASOS):
    """Arma el Pipeline con los pasos descubiertos en el grupo."""
    pasos = descubrir_pasos(grupo)
    if not pasos:
        raise RuntimeError(f"No hay pasos registrados en el grupo '{grupo}'.")
    return Pipeline(pasos)
