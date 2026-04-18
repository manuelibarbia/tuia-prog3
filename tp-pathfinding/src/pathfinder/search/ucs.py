from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Uniform Cost Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize root node
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)

        # Inicializamos alcanzados con el estado inicial
        reached = {}
        reached[root.state] = root.cost

        # Inicializamos la frontera con una cola de prioridades
        frontera = PriorityQueueFrontier()
        frontera.add(root, priority=root.cost)

        # Mientras la cola de prioridades NO esté vacía, seguí explorando
        while not frontera.is_empty():

            # Sacamos el nodo con el menor costo acumulado g(n)
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

                # Solo avanzamos si el estado nunca fue alcanzado o si encontramos un camino más barato
                if nuevo_estado not in reached or nuevo_costo < reached[nuevo_estado]:
                    # Actualizamos el mejor costo conocido para este estado
                    reached[nuevo_estado] = nuevo_costo

                    # Creamos el nodo hijo
                    nodo_hijo = Node("", state=nuevo_estado, cost=nuevo_costo, parent=nodo_estudio, action=action)

                    # Lo añadimos a la cola de prioridades con el costo (sin heurística)
                    frontera.add(nodo_hijo, priority=nuevo_costo)

        return NoSolution(reached)
