from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class GreedyBestFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Greedy Best First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize root node
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)

        # Calculamos la heurística para el nodo raíz
        root.estimated_distance = grid.heuristica(root.state)

        # Inicializamos alcanzados con el estado inicial
        reached = {}
        reached[root.state] = root.cost

        # Inicializamos la frontera con una cola de prioridades
        frontera = PriorityQueueFrontier()
        frontera.add(root, priority=root.estimated_distance)

        # Mientras la cola de prioridades NO esté vacía, seguí explorando
        while not frontera.is_empty():

            # Sacamos el nodo con el menor valor heurístico h(n)
            nodo_estudio = frontera.pop()

            # Si este nodo ES el objetivo, devolvemos la solución
            if grid.objective_test(nodo_estudio.state):
                return Solution(nodo_estudio, reached)
            
            # Si NO, exploramos sus vecinos
            for action in grid.actions(nodo_estudio.state):
                # Calculamos el nuevo estado después de la acción
                nuevo_estado = grid.result(nodo_estudio.state, action)

                # Calculamos el costo
                costo_mov = grid.individual_cost(nodo_estudio.state, action)
                nuevo_costo = nodo_estudio.cost + costo_mov

                # Solo avanzamos si este estado nunca fue visitado
                if nuevo_estado not in reached:
                    # Marcamos como alcanzado
                    reached[nuevo_estado] = nuevo_costo

                    # Creamos el nodo hijo
                    nodo_hijo = Node("", state=nuevo_estado, cost=nuevo_costo, parent=nodo_estudio, action=action)

                    # Calculamos la heurística (solo h(n), sin costo acumulado)
                    h = grid.heuristica(nuevo_estado)
                    nodo_hijo.estimated_distance = h

                    # Lo añadimos a la cola de prioridades con la heurística
                    frontera.add(nodo_hijo, priority=h)

        return NoSolution(reached)
