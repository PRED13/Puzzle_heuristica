from django.shortcuts import render
from .logic.arbol import Nodo
from .logic.puzzle_logic import buscar_solucion_heuristica

def index(request):
    resultado = None
    error = None
    
    if request.method == "POST":
        try:
            # Convertir string "4,2,3,1" a lista de enteros [4, 2, 3, 1]
            inicio = [int(x.strip()) for x in request.POST.get("inicio").split(",")]
            meta = [int(x.strip()) for x in request.POST.get("meta").split(",")]
            
            nodo_inicial = Nodo(inicio)
            sol_nodo = buscar_solucion_heuristica(nodo_inicial, meta, [])
            
            if sol_nodo:
                resultado = []
                while sol_nodo:
                    resultado.append(sol_nodo.get_datos())
                    sol_nodo = sol_nodo.get_padre()
                resultado.reverse()
            else:
                error = "No se encontró una solución bajo esta heurística."
        except Exception as e:
            error = f"Error en los datos: {str(e)}"

    return render(request, "solver/index.html", {"resultado": resultado, "error": error})