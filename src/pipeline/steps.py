"""Fabricas de los pasos del Pipeline, declaradas como entrypoints.

Cada funcion devuelve la tupla (nombre, estimador) que espera scikit-learn.
"""
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler


def imputer():
    """Imputa los valores faltantes con la mediana."""
    return "imputer", SimpleImputer(strategy="median")


def scaler():
    """Estandariza las columnas."""
    return "scaler", StandardScaler()


def pca():
    """Reduce dimensiones conservando el 95% de la varianza."""
    return "pca", PCA(n_components=0.95)
