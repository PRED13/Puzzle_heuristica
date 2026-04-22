# 🧩 Puzzle Heurística

## 📋 Descripción del Proyecto

Se desarrolló un sistema web interactivo para resolver puzzles lineales mediante búsqueda heurística. La aplicación, construida con <span style="color:#FF6B6B">**Django**</span>, permite al usuario ingresar un estado inicial y un estado objetivo, y utiliza un algoritmo de búsqueda informada para encontrar la secuencia de movimientos que llevan de uno a otro.

## ⚙️ ¿Qué se hizo?

1. **🌐 Interfaz Web**: Se creó un formulario HTML que permite al usuario:
   - Ingresar el estado inicial del puzzle (ej: 4,2,3,1)
   - Especificar el estado objetivo (ej: 1,2,3,4)
   - Visualizar la solución como una secuencia de estados

2. **🌳 Estructura de Datos**: Se implementó un árbol de búsqueda mediante la clase <span style="color:#4ECDC4">**`Nodo`**</span> que:
   - Almacena los datos (estado del puzzle)
   - Mantiene referencias a nodos hijos (estados generados)
   - Rastrea el nodo padre (para reconstruir la solución)

3. **🔄 Generación de Movimientos**: Para cada estado se generan 3 movimientos posibles (intercambios):
   - Intercambiar posiciones 0 y 1
   - Intercambiar posiciones 1 y 2
   - Intercambiar posiciones 2 y 3

4. **🔒 Búsqueda con Visitados**: Se implementó un mecanismo para evitar revisitar estados, previniendo ciclos infinitos.

## 📐 Modelo Matemático: Búsqueda Heurística (Hill Climbing)

### 🎯 Fundamento Teórico

El algoritmo implementado pertenece a la familia de búsquedas **informadas** o **guiadas** conocidas como <span style="color:#FFD93D">**Hill Climbing**</span> (Escalada de Colinas). Este es un tipo de búsqueda local que utiliza una **función heurística** para evaluar la calidad de cada estado.

### 🧮 Función Heurística

La heurística utilizada mide la <span style="color:#6BCB77">**"calidad de orden"**</span> de un estado contando el número de pares consecutivos donde el elemento actual es mayor que el anterior (subsecuencias ascendentes):

$$h(estado) = \sum_{i=1}^{n-1} \begin{cases} 1 & \text{si } estado[i] > estado[i-1] \\ 0 & \text{en caso contrario} \end{cases}$$

**Interpretación**: Un estado con una heurística más alta tiene más elementos en orden ascendente, aproximándose más al objetivo [1,2,3,4].

### 🎲 Estrategia de Búsqueda

El algoritmo sigue la estrategia <span style="color:#FF6B6B">**"solo aceptar mejora"**</span> (only-accept-improvement):
- Genera todos los estados vecinos (hijos) posibles
- Solo explora un nodo hijo si: `h(hijo) ≥ h(padre)`
- Se detiene cuando encuentra el estado objetivo
- Usa una lista de visitados para evitar ciclos

### ✅ Función de Decisión

```
mejora(padre, hijo) = (h(hijo) ≥ h(padre)) AND (hijo ∉ visitados)
```

Donde `visitados` es el conjunto de estados ya explorados.

## 💻 Aplicación al Código

### 🌳 Implementación del Árbol (arbol.py)

```python
class Nodo:
    def __init__(self, datos, hijos=None):
        self.datos = datos      # Estado actual
        self.hijos = None       # Estados generados (vecinos)
        self.padre = None       # Referencia para reconstruir camino
```

Cada nodo representa un estado del puzzle. La relación padre-hijo forma el árbol de búsqueda.

### 🧮 Implementación de la Heurística (puzzle_logic.py)

```python
def mejora(nodo_padre, nodo_hijo):
    calidad_padre = 0
    calidad_hijo = 0
    
    for n in range(1, len(dato_padre)):
        if dato_padre[n] > dato_padre[n-1]:    
            # Contar pares ascendentes
            calidad_padre += 1
        if dato_hijo[n] > dato_hijo[n-1]:
            calidad_hijo += 1
    
    return calidad_hijo >= calidad_padre       
    # Solo aceptar mejora
```

Esta función implementa la comparación de la heurística.

### 🔍 Búsqueda Recursiva (puzzle_logic.py)

```python
def buscar_solucion_heuristica(nodo_inicial, solucion, visitados):
    visitados.append(nodo_inicial.get_datos())  # Marcar como visitado
    
    if nodo_inicial.get_datos() == solucion:    # Condición de parada
        return nodo_inicial
    
    # Generar 3 movimientos (vecinos)
    hijos_datos = [
        [nodo[1], nodo[0], nodo[2], nodo[3]],   # Intercambio 0-1
        [nodo[0], nodo[2], nodo[1], nodo[3]],   # Intercambio 1-2
        [nodo[0], nodo[1], nodo[3], nodo[2]]    # Intercambio 2-3
    ]
    
    for nodo_hijo in hijos:
        # Solo explorar si mejora Y no está visitado
        if nodo_hijo not in visitados and mejora(nodo_inicial, nodo_hijo):
            sol = buscar_solucion_heuristica(nodo_hijo, solucion, visitados)
            if sol is not None:
                return sol
```

Este algoritmo implementa la búsqueda Hill Climbing recursivamente, garantizando exploración solo de caminos prometedores.

### 🌐 Interfaz Web (views.py)

La vista <span style="color:#FF6B6B">**Django**</span> recibe los datos del formulario, instancia el árbol de búsqueda y reconstruye el camino completo desde la raíz hasta la solución encontrada.

## ⚠️ Limitaciones y Consideraciones

- <span style="color:#FF6B6B">**⛔ No garantiza solución global**</span>: Hill Climbing puede quedar atrapado en óptimos locales
- <span style="color:#FFD93D">**⚡ Orden de generación importante**</span>: La secuencia en que se generan los hijos afecta el resultado
- <span style="color:#4ECDC4">**📊 Complejidad**</span>: Depende de la profundidad del árbol de soluciones
