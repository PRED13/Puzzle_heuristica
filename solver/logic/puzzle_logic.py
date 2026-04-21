from .arbol import Nodo

def mejora(nodo_padre, nodo_hijo):
    calidad_padre = 0
    calidad_hijo = 0
    dato_padre = nodo_padre.get_datos()
    dato_hijo = nodo_hijo.get_datos()

    for n in range(1, len(dato_padre)):
        if dato_padre[n] > dato_padre[n-1]:
            calidad_padre += 1
        if dato_hijo[n] > dato_hijo[n-1]:
            calidad_hijo += 1
    return calidad_hijo >= calidad_padre

def buscar_solucion_heuristica(nodo_inicial, solucion, visitados):
    visitados.append(nodo_inicial.get_datos())
    if nodo_inicial.get_datos() == solucion:
        return nodo_inicial
    
    dato_nodo = nodo_inicial.get_datos()
    # Generación de movimientos (Hijos)
    hijos_datos = [
        [dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]],
        [dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]],
        [dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]]
    ]
    
    hijos = [Nodo(h) for h in hijos_datos]
    nodo_inicial.set_hijos(hijos)

    for nodo_hijo in nodo_inicial.get_hijos():
        if nodo_hijo.get_datos() not in visitados and mejora(nodo_inicial, nodo_hijo):
            sol = buscar_solucion_heuristica(nodo_hijo, solucion, visitados)
            if sol is not None:
                return sol
    return None