# clasificacion_variables.py — Parte A: clasificación de las variables de clientes.csv.
#
# El archivo data/clientes.csv tiene 12 clientes y 7 variables (más el id).
# El objetivo: clasificar cada variable (numérica continua/discreta, categórica
# binaria/ordinal/nominal) y verificar la clasificación en código.
#
# Regla del capítulo 3: el dtype es una pista, no la clasificación — el criterio
# (¿tiene sentido la mitad del valor? ¿hay orden entre las categorías?) decide.
#
# Uso (desde la raíz del repositorio):  python scripts/clasificacion_variables.py

import pandas as pd

clientes = pd.read_csv("data/clientes.csv")

# ---------------------------------------------------------------------------
# 1. Estructura del archivo
# ---------------------------------------------------------------------------
print(f"Dimensiones: {clientes.shape[0]} filas × {clientes.shape[1]} columnas")
print()
print("Primeras filas:")
print(clientes.to_string(index=False))
print()

# ---------------------------------------------------------------------------
# 2. Tipos inferidos (dtype) — la pista que da el lenguaje
# ---------------------------------------------------------------------------
print("Tipos inferidos (dtype):")
print(clientes.dtypes)
print()
# TODO 1: ¿qué columnas llegan como número y cuáles como texto? Anótalo para el
#         informe. Ojo con satisfaccion: llega como número y es ordinal
#         ("4 no es el doble de 2") — la justificación va en el informe.

# ---------------------------------------------------------------------------
# 3. Valores únicos — ¿cuántas categorías hay y cuáles son?
# ---------------------------------------------------------------------------
# TODO 2: completa el bucle para imprimir, por columna, cuántos valores únicos
#         hay y cuáles son. Pista: for columna in clientes.columns: ...  con
#         clientes[columna].unique() y len(). ¿Cuántas categorías tiene genero?
print("Valores únicos por columna:")
for columna in clientes.columns:
    unicos = clientes[columna].unique()
    print(f"  Columna: {columna:20s} | Cantidad: {len(unicos)} | Valores: {unicos}")
print()

# ---------------------------------------------------------------------------
# 4. Declarar el orden de las variables ordinales
# ---------------------------------------------------------------------------
# Una ordinal se guarda como texto (o como número) y su orden natural se pierde:
# alfabéticamente "Posgrado" iría antes que "Primaria", que no tiene sentido.
#
# TODO 3: convierte nivel_educacion a categoría ordenada.
#         Pista: astype(pd.CategoricalDtype(categories=[...], ordered=True)).
#         Comprueba con .min(): debe devolver "Primaria".
orden_educacion = ["Primaria", "Secundaria", "Universidad", "Posgrado"]
clientes["nivel_educacion"] = clientes["nivel_educacion"].astype(
    pd.CategoricalDtype(categories=orden_educacion, ordered=True)
)
print(f"Mínimo nivel de educación: {clientes['nivel_educacion'].min()}")

# TODO 4: haz lo mismo con satisfaccion (escala 1–5 como etiquetas ordenadas).
#         Prueba extra: ¿qué pasa si en la lista de categorías escribes
#         "Postgrado" (con t) para nivel_educacion? Cuenta los faltantes con
#         .isna().sum() — la trampa del typo es silenciosa.
orden_satisfaccion = [1, 2, 3, 4, 5]
clientes["satisfaccion"] = clientes["satisfaccion"].astype(
    pd.CategoricalDtype(categories=orden_satisfaccion, ordered=True)
)
print(f"Mínima satisfacción: {clientes['satisfaccion'].min()}")
print(f"Valores faltantes en nivel_educacion: {clientes['nivel_educacion'].isna().sum()}")
print()

# ---------------------------------------------------------------------------
# 5. Resumen de la clasificación (para el informe)
# ---------------------------------------------------------------------------
# TODO 5: completa el resumen con el tipo de cada variable (el criterio que
#         justifica cada clasificación va en el informe).
clasificacion = {
    "cliente_id": "Categorica nominal (Identificador)",
    "edad": "Numerica discreta",
    "numero_hijos": "Numerica discreta",
    "genero": "Categorica nominal",
    "nivel_educacion": "Categorica ordinal",
    "ciudad": "Categorica nominal",
    "ingresos_mensuales": "Numerica continua",
    "satisfaccion": "Categorica ordinal",
}
print("Resumen de la clasificación (para el informe):")
for variable, tipo in clasificacion.items():
    print(f"  {variable:20s} {tipo}")