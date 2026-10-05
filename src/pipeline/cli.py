"""Punto de entrada de consola, declarado en [project.scripts]."""
import argparse

import pandas as pd

from .core import (
    GRUPO_PASOS,
    crear_pipeline,
    descubrir_pasos,
    filtrar_datos,
    obtener_datos,
    separar_datos,
)


def main():
    """Ejecuta el pipeline, o lista los pasos registrados."""
    parser = argparse.ArgumentParser(prog="pipeline-sklearn")
    parser.add_argument("--csv", help="Ruta a un CSV local en lugar de descargarlo.")
    parser.add_argument(
        "--listar-pasos",
        action="store_true",
        help="Muestra los pasos registrados en el grupo y termina.",
    )
    args = parser.parse_args()

    if args.listar_pasos:
        for nombre, estimador in descubrir_pasos():
            print(f"{nombre}: {type(estimador).__name__}")
        return

    datos = pd.read_csv(args.csv) if args.csv else obtener_datos()
    X_train, X_val, X_test = separar_datos(filtrar_datos(datos))

    pipeline = crear_pipeline()
    X_train_t = pipeline.fit_transform(X_train)

    print(f"grupo de pasos: {GRUPO_PASOS}")
    print(f"pasos descubiertos: {[n for n, _ in pipeline.steps]}")
    print(f"filas entrenamiento/validacion/prueba: {len(X_train)}/{len(X_val)}/{len(X_test)}")
    print(f"columnas antes: {X_train.shape[1]}  despues de PCA: {X_train_t.shape[1]}")
