# Pipeline de scikit-learn con entrypoints

Pipeline de preparacion de datos cuyos pasos no estan escritos en el codigo: se
descubren en tiempo de ejecucion a partir de los entrypoints que declaran los
paquetes instalados.

Adaptacion del pipeline de la actividad 01 del curso de Machine Learning
Engineering, hecha para la actividad 09 sobre entrypoints de Python.

## Que demuestra

- Un entrypoint de `[project.scripts]` que crea el comando `pipeline-sklearn`
  en el entorno, invocable por nombre y no por ruta de archivo.
- Un grupo propio, `pipeline.steps`, del que `crear_pipeline` lee los pasos con
  `importlib.metadata.entry_points`.
- Que instalar un segundo paquete agrega un paso al Pipeline sin modificar ni
  reinstalar el paquete principal.

## Estructura

```text
src/pipeline/
├── steps.py      # fabricas de los pasos, declaradas como entrypoints
├── core.py       # carga de datos y construccion del Pipeline desde el grupo
└── cli.py        # funcion main a la que apunta el comando de consola
plugin_extra/     # paquete aparte que agrega un paso al mismo grupo
Makefile          # targets que invocan el comando instalado
```

## Instalacion

```bash
python3 -m venv .venv
source .venv/bin/activate      # en Windows: .venv\Scripts\activate
pip install -e .
```

## Uso

Listar los pasos registrados en el grupo:

```bash
pipeline-sklearn --listar-pasos
```

```text
imputer: SimpleImputer
scaler: StandardScaler
pca: PCA
```

Ejecutar el pipeline. Sin argumentos descarga el CSV; con `--csv` usa un archivo
local:

```bash
pipeline-sklearn
```

```text
grupo de pasos: pipeline.steps
pasos descubiertos: ['imputer', 'scaler', 'pca']
filas entrenamiento/validacion/prueba: 396/132/132
columnas antes: 5  despues de PCA: 4
```

## Extender el pipeline sin tocarlo

`plugin_extra` es un paquete independiente que declara un paso en el grupo
`pipeline.steps`. El prefijo `25` de su nombre lo coloca entre el escalado y el
PCA.

```bash
pip install -e plugin_extra
pipeline-sklearn --listar-pasos
```

```text
imputer: SimpleImputer
scaler: StandardScaler
varianza: VarianceThreshold
pca: PCA
```

El paquete principal no se modifico ni se reinstalo.

## Declaracion de los entrypoints

```toml
[project.scripts]
pipeline-sklearn = "pipeline.cli:main"

[project.entry-points."pipeline.steps"]
10-imputer = "pipeline.steps:imputer"
20-scaler = "pipeline.steps:scaler"
30-pca = "pipeline.steps:pca"
```

Al instalar, el backend las escribe en `entry_points.txt` dentro del directorio
`.dist-info` del paquete:

```text
[console_scripts]
pipeline-sklearn = pipeline.cli:main

[pipeline.steps]
10-imputer = pipeline.steps:imputer
20-scaler = pipeline.steps:scaler
30-pca = pipeline.steps:pca
```

## Makefile

Los targets llaman al comando instalado en lugar de rutas de archivo. La
instalacion es prerrequisito de los demas, porque el comando no existe hasta que
el paquete esta instalado.

```bash
make pasos     # instala y lista los pasos
make run       # instala y ejecuta el pipeline
make extra     # instala el paquete adicional y vuelve a listar
make limpiar   # desinstala ambos paquetes
```

## Referencias

- [Especificacion de entry points](https://packaging.python.org/en/latest/specifications/entry-points/)
- [Creacion y descubrimiento de plugins](https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/)
- [Makefile y GitHub Actions](https://www.datacamp.com/tutorial/makefile-github-actions-tutorial)
