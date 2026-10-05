"""Paso adicional registrado en el grupo pipeline.steps."""
from sklearn.feature_selection import VarianceThreshold


def varianza():
    """Descarta columnas de varianza casi nula."""
    return "varianza", VarianceThreshold(threshold=0.01)
