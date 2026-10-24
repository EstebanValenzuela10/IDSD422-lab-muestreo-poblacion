# Informe — Clasificación de variables y población vs. muestra

**Para:** Gerencia de RetailAndina S.A. · **De:** Equipo de Business Intelligence
**Fecha:** 23/10/2026 · **Asunto:** Base de fidelización: tipos de variables y estimación por muestreo

---

## Resumen ejecutivo

Se clasificaron las 7 variables de la base de fidelización y se verificó la clasificación en código: `satisfaccion` llega como número (`int64`) pero es ordinal, y `nivel_educacion` llega como texto sin orden. Se quiso estimar el ingreso mensual promedio de los 400 clientes (parámetro: 1 330,72) con muestras de 20, usando tres diseños: conveniencia, aleatorio simple y estratificado. La muestra por conveniencia tomó 20 clientes de Quito y su media quedó cerca solo por casualidad; las medias del aleatorio simple variaron entre 1 235,00 y 1 491,50 según la semilla. Antes de decidir con una muestra, la gerencia debe conocer cómo se eligió y que una sola cifra puede cambiar con otro sorteo.

## Parte A — Clasificación de las variables

| Variable | Tipo | Justificación (criterio) | Verificación en código |
|---|---|---|---|
| `cliente_id` | Identificador (categórica nominal) | Es solo un código para distinguir a cada cliente. No tiene sentido sumarlo, promediarlo ni calcular su mitad. | `object`; 12 únicos en 12 filas |
| `edad` | Numérica discreta | La base la registra en años cumplidos (22, 27, 34), sin fracciones. La mitad (17 años) sí tiene sentido y 0 es ausencia, por eso es de razón. La edad real es continua, pero aquí se mide en enteros, por lo que la traté como discreta. | `int64`; 12 únicos; rango 22 a 48 |
| `numero_hijos` | Numérica discreta | Es un conteo: se cuentan hijos enteros. No existe un cliente con 2,5 hijos. | `int64`; 5 únicos (0 a 4) |
| `genero` | Categórica nominal | Son categorías (Femenino, Masculino, Otro) y ninguna va antes que otra. Solo sirven para agrupar. | `object`; 3 únicos (Femenino, Masculino, Otro) |
| `nivel_educacion` | Categórica ordinal | Hay orden (Primaria < Secundaria < Universidad < Posgrado), pero no una distancia fija ni una «mitad». | `object`; 4 únicos; orden declarado; mínimo = Primaria |
| `ciudad` | Categórica nominal | Son nombres de lugares (Quito, Guayaquil, Cuenca) y ninguna ciudad va antes que otra. Solo sirven para agrupar. | `object`; 3 únicos |
| `ingresos_mensuales` | Numérica continua | Es un monto de dinero, tiene sentido su mitad y puede tomar cualquier valor, no solo enteros (por ejemplo, 1 450,50). | `int64`; 12 únicos; rango 760 a 2 450 |
| `satisfaccion` | Categórica ordinal | Aunque son números (2 a 5), representan una opinión con orden: 5 es más satisfecho que 4. Pero no se sabe si la diferencia entre 4 y 5 es igual a la de 2 y 3, y la mitad de 4 no significa nada. Los números son solo etiquetas. | `int64` (engaña); 4 únicos (2, 3, 4, 5); mínimo = 2 |

**P1.** ¿Qué te dijo el dtype de `satisfaccion` y por qué no basta para clasificarla? ¿Qué pasa si una ordinal queda como texto sin declarar el orden?

Como se puede observar en la Figura 1, pandas la leyó como número (`int64`). Pero el dtype describe cómo se guardó el dato, no qué significa. Los valores únicos son 4, 3, 5 y 2 (Figura 2), una escala de opinión en la que no sé si la distancia de 4 a 5 equivale a la de 2 a 3, así que promediarla sería erróneo. Con `nivel_educacion` pasó lo contrario: llegó como `object` (texto) y sus valores únicos aparecen en orden de aparición (Universidad, Secundaria, Posgrado, Primaria), sin jerarquía. Si queda como texto sin declarar el orden, un máximo, un mínimo o un ordenamiento usaría el orden alfabético (Posgrado antes que Primaria) y daría resultados falsos. Al declarar el orden, el mínimo salió Primaria, como corresponde.

## Parte B — Población vs. muestra

### La población y su parámetro

| Concepto | Valor |
|---|---|
| Población (N) | 400 clientes (Quito 200 / Guayaquil 120 / Cuenca 80) |
| Variable de interés | `ingresos_mensuales` (numérica continua) |
| Parámetro poblacional (media) | 1 330,725 |

*¿Por qué se muestrea si aquí el parámetro existe y se calculó?* Aquí lo calculé porque tenía los 400 registros, y sirve para evaluar los diseños. En la práctica la empresa no tendría todos los ingresos (o medirlos costaría tiempo y dinero) y el parámetro sería desconocido: la muestra sirve para estimarlo.

### Los tres diseños

| Diseño | n | Media estimada | Composición por ciudad | Diferencia vs. parámetro |
|---|---|---|---|---|
| Conveniencia (`head`) | 20 | 1 348,50 | Quito 20 · Guayaquil 0 · Cuenca 0 | +17,78 |
| Aleatorio simple (`sample`) | 20 | 1 336,00 | Quito 8 · Guayaquil 4 · Cuenca 8 | +5,28 |
| Estratificado (`groupby` + 5 %) | 20 | 1 287,50 | Quito 10 · Guayaquil 6 · Cuenca 4 | −43,22 |

| Semilla | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Media | 1 336,00 | 1 405,00 | 1 235,00 | 1 491,50 | 1 288,00 |

**P2.** ¿Cuánto vale el parámetro poblacional y cuánto estimó cada diseño? ¿Cuál quedó más cerca y por qué eso **no** alcanza para declarar un ganador?

El parámetro es 1 330,72. La conveniencia estimó 1 348,50 (+17,78), el aleatorio simple 1 336,00 (+5,28) y el estratificado 1 287,50 (−43,22). El aleatorio simple quedó más cerca en ambos lenguajes, pero eso no alcanza para determinarlo como mejor: es una sola corrida por lenguaje, y el estratificado, que tuvo la composición más parecida a la población (10/6/4), fue el más lejano en las dos. Con otra semilla el orden cambia. Además, la conveniencia quedó más cerca que el estratificado siendo el diseño defectuoso: acercarse al parámetro por casualidad no prueba que el método sea válido.

**P3.** La muestra por conveniencia también tiene 20 filas. ¿Qué defecto tiene y cómo lo delatas en la composición por ciudad? ¿Se corrige tomando más filas?

En esta parte `head(20)` devolvió los primeros 20 registros, y el archivo está ordenado por ciudad: los 20 son de Quito (Figura 3), que es el 50 % de la población, y Guayaquil y Cuenca quedaron con 0. Lo delató la composición por ciudad. Es un sesgo sistemático: en la población, Quito promedia 1 390,50 y Cuenca 1 193,50, así que esta muestra tiende a sobreestimar, unos +60 sobre el parámetro. Que su media diera +17,78 fue suerte dentro de Quito, no mérito del método. Con más filas no se corrige: `head(100)` seguiría siendo solo Quito, y `head(200)` también; el defecto está en cómo se eligió, no en cuántos se eligieron.

**P4.** El sorteo aleatorio dio un número distinto en cada semilla. ¿Qué implica esa variabilidad para una empresa que va a decidir con un solo estudio?

Implica que un estudio con n = 20 es una de muchas medias posibles: con las semillas 1 a 5 obtuve entre 1 235,00 y 1 491,50, un rango de 256,50. Incluso el mismo diseño dio 1 336,00 en Python y 1 318,00 en R, porque los generadores y semillas producen sorteos distintos. A diferencia del sesgo de la conveniencia, esta variabilidad no es sistemática: se compensa en promedio y baja con una muestra más grande.

**P5.** ¿Cuándo usarías cada diseño en la práctica? Relaciona cada uno con un uso real (piloto, subgrupos que deben aparecer, conclusión sobre toda la población).

- **Conveniencia:** para una exploración rápida o un piloto (probar un cuestionario, ver cómo se ven los datos), sin generalizar a toda la población.
- **Aleatorio simple:** cuando hay que concluir sobre toda la población y no hay subgrupos críticos; cada cliente tiene la misma probabilidad de entrar.
- **Estratificado:** cuando hay subgrupos que deben aparecer en su proporción. En 1 000 repeticiones su desviación fue 86,60, similar a la del aleatorio simple (89,60), y garantiza que ninguna ciudad quede sin representar.

## Conclusiones

1. De las 7 variables, 3 son numéricas (`edad` y `numero_hijos` discretas; `ingresos_mensuales` continua), 2 son categóricas nominales (`genero`, `ciudad`) y 2 son categóricas ordinales (`nivel_educacion` con 4 niveles y `satisfaccion` con valores 2 a 5). El dtype solo ayudó con las numéricas; `satisfaccion` (`int64`) y `nivel_educacion` (texto) requirieron declarar el orden.

2. El parámetro es 1 330,72 (N = 400). La conveniencia (1 348,50) tomó 20 de 20 clientes de Quito, frente al 50 % de la población, con un sesgo esperado de unos +60 que no se corrige con más filas. El aleatorio simple (1 336,00; +5,28) y el estratificado (1 287,50; −43,22) usaron clientes de las tres ciudades.

3. Con n = 20, las medias aleatorias fueron de 1 235,00 a 1 491,50 (semillas 1–5) y, en 1 000 sorteos, la desviación fue 90. Esa variabilidad es del sorteo y se reduce con n; el sesgo es del diseño y no.

**Respuesta a la gerencia y alcance.** Con esta base de 400 clientes de Quito, Guayaquil y Cuenca, una muestra de 20 clientes elegida al azar o estratificada por ciudad puede estimar el ingreso mensual promedio con un error típico cercano a 90; una muestra por conveniencia no sirve para esa conclusión. Estos resultados aplican a esta base y a estos diseños, no a otras ciudades ni a otros períodos. La lección central: el diseño decide, no el tamaño.