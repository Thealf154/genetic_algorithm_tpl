import random

# Definición de la matriz de distancias
paths = [
    [0,15,8,23,5,9,14,23,3,18,7,8,11,20,8],
    [15,0,17,28,24,28,16,23,15,12,17,20,33,21,17],
    [8,17,0,27,9,21,13,21,11,9,3,11,18,14,4],
    [23,28,27,0,20,25,34,51,19,30,24,17,27,18,28],
    [5,24,9,20,0,7,23,39,4,19,13,13,10,5,17],
    [9,28,21,25,7,0,26,38,8,22,17,12,5,9,21],
    [14,16,13,34,23,26,0,13,18,6,11,12,35,22,11],
    [23,23,21,51,39,38,13,0,26,21,20,27,36,31,19],
    [3,15,11,19,4,8,18,26,0,14,8,4,11,4,12],
    [18,12,9,30,19,22,6,21,14,0,8,15,29,19,6],
    [7,17,3,24,13,17,11,20,8,8,0,9,23,13,5],
    [8,20,11,17,9,12,12,27,4,15,9,0,17,5,15],
    [11,33,18,27,10,5,35,36,11,29,23,17,0,17,20],
    [20,21,14,18,5,9,22,31,4,19,13,5,17,0,16],
    [8,17,4,28,17,21,11,19,12,6,5,15,20,16,0],
]

# Parámetros del algoritmo genético
TAM_POBLACION = 30
NUM_GENERACIONES = 100
PROB_CRUZAMIENTO = 0.8
PROB_MUTACION = 0.1

# Función objetivo (a ser minimizada)
def funcion_objetivo(individuo):
    distancia_total = 0
    for i in range(len(individuo)-1):
        origen = individuo[i]
        destino = individuo[i+1]
        distancia_total += paths[origen][destino]####dafak
    return distancia_total

# Evaluación de la población
def evaluar_poblacion(poblacion):
    evaluaciones = [] #creas un array de evaluaciones
    for individuo in poblacion:
        evaluaciones.append(funcion_objetivo(individuo))
    return evaluaciones

# Selección de individuos mediante torneo binario
def seleccion(poblacion, evaluaciones):
    seleccionados = []
    for _ in range(len(poblacion)):
        candidato1 = random.choice(poblacion)
        candidato2 = random.choice(poblacion)
        evaluacion1 = evaluaciones[poblacion.index(candidato1)]
        evaluacion2 = evaluaciones[poblacion.index(candidato2)]
        seleccionado = candidato1 if evaluacion1 < evaluacion2 else candidato2
        seleccionados.append(seleccionado)
    return seleccionados

# Cruzamiento de dos individuos mediante orden basado en puntos de corte
def cruzamiento(individuo1, individuo2):
    cromosoma1 = individuo1
    cromosoma2 = individuo2
    punto_corte1 = random.randint(0, len(cromosoma1) - 2)
    punto_corte2 = random.randint(punto_corte1 + 1, len(cromosoma1) - 1)

    hijo1 = cromosoma1[:punto_corte1] + cromosoma2[punto_corte1:punto_corte2] + cromosoma1[punto_corte2:]
    hijo2 = cromosoma2[:punto_corte1] + cromosoma1[punto_corte1:punto_corte2] + cromosoma2[punto_corte2:]

    return hijo1, hijo2

# Mutación de un individuo mediante intercambio de dos genes
def mutacion(individuo):
    cromosoma = individuo
    indice1 = random.randint(0, len(cromosoma) - 1)
    indice2 = random.randint(0, len(cromosoma) - 1)

    cromosoma[indice1], cromosoma[indice2] = cromosoma[indice2], cromosoma[indice1]

    return cromosoma

# Renovación generacional
def renovacion_generacional(poblacion, evaluaciones, nueva_generacion):
    for i in range(len(nueva_generacion)):
        peor_individuo = poblacion[evaluaciones.index(max(evaluaciones))]
        indice_peor = poblacion.index(peor_individuo)
        poblacion[indice_peor] = nueva_generacion[i]
        evaluaciones[indice_peor] = evaluaciones[i]

# Algoritmo genético
def algoritmo_genetico():
    # Generación de la población inicial
    poblacion = []
    evaluaciones = []
    for _ in range(TAM_POBLACION):
        base = [x for x in range(len(paths))]
        random.shuffle(base)
        poblacion.append(base)

    # Ciclo de generaciones
    for _ in range(NUM_GENERACIONES):
        # Evaluación de la población actual
        evaluaciones = evaluar_poblacion(poblacion)

        # Creación de la nueva generación
        nueva_generacion = []

        # Selección
        seleccionados = seleccion(poblacion, evaluaciones)

        # Cruzamiento
        for i in range(0, len(seleccionados), 2):
            if random.random() < PROB_CRUZAMIENTO:
                hijo1, hijo2 = cruzamiento(seleccionados[i], seleccionados[i+1])
                nueva_generacion.append(hijo1)
                nueva_generacion.append(hijo2)
            else:
                nueva_generacion.append(seleccionados[i])
                nueva_generacion.append(seleccionados[i+1])

        # Mutación
        for i in range(len(nueva_generacion)):
            if random.random() < PROB_MUTACION:
                nueva_generacion[i] = mutacion(nueva_generacion[i])

        # Renovación generacional
        renovacion_generacional(poblacion, evaluaciones, nueva_generacion)

    # Mejor individuo encontrado
    mejor_individuo = poblacion[evaluaciones.index(min(evaluaciones))]
    mejor_camino = mejor_individuo

    return mejor_camino

# Ejecución del algoritmo genético
mejor_camino = algoritmo_genetico()
print("Mejor camino encontrado:", mejor_camino)
print("Distancia mínima:", funcion_objetivo(mejor_camino))
