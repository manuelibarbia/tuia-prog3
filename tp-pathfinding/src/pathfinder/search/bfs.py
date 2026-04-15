from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Breadth First Search"""
        
        # Initialize root node
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)

        # Initialize reached with the initial state
        reached = {}
        reached[root.state] = True

        # 1. Inicializamos la frontera y agregamos el nodo raíz
        frontera = QueueFrontier()
        frontera.add(root)

        # 2. Mientras la cola NO esté vacía, seguimos explorando
        while not frontera.is_empty():
            
            # 3. Sacamos el nodo más antiguo de la cola (FIFO)
            nodo_estudio = frontera.remove()

            # 4. Si el nodo que estamos estudiando ES el objetivo, devolvemos la solución
            if grid.objective_test(nodo_estudio.state):
                return Solution(nodo_estudio, reached)

            # 5. Si NO es la meta, exploramos sus vecinos (arriba, abajo, izquierda, derecha)
            for action in grid.actions(nodo_estudio.state):
                
                # Calculamos en qué coordenadas caería con esa acción
                nuevo_estado = grid.result(nodo_estudio.state, action)

                # 6. Solo avanzamos si esta baldosa NUNCA la pisamos antes
                # En BFS no nos importa actualizar costos menores como en A*, 
                # porque el primer camino que encuentra hacia un nodo siempre es el más corto en pasos.
                if nuevo_estado not in reached:
                    # Calculamos el costo primero
                    costo_mov = grid.individual_cost(nodo_estudio.state, action)
                    nuevo_costo = nodo_estudio.cost + costo_mov

                    # Guardamos el número en lugar de True
                    reached[nuevo_estado] = nuevo_costo
                    
                    # Calculamos el costo del movimiento y lo sumamos al acumulado
                    costo_mov = grid.individual_cost(nodo_estudio.state, action)
                    nuevo_costo = nodo_estudio.cost + costo_mov

                    # Creamos el nuevo Nodo Hijo
                    nodo_hijo = Node("", state=nuevo_estado, cost=nuevo_costo, parent=nodo_estudio, action=action)

                    # 7. Lo mandamos al FINAL de la cola para explorarlo cuando llegue su turno
                    frontera.add(nodo_hijo)

        # Si la cola se vacía y nunca encontró la meta, no hay solución
        return NoSolution(reached)