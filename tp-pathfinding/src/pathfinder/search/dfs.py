from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Depth First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize root node
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)

        # Initialize reached with the initial state
        reached = {}
        reached[root.state] = True

        # Inicializamos la frontera con una pila (LIFO)
        frontera = StackFrontier()
        frontera.add(root)

        # Mientras la pila NO esté vacía, seguí explorando
        while not frontera.is_empty():
            
            # Sacamos el nodo más reciente de la pila (LIFO)
            nodo_estudio = frontera.remove()

            # Si este nodo ES el objetivo, devolvemos la solución
            if grid.objective_test(nodo_estudio.state):
                return Solution(nodo_estudio, reached)

            # Si NO, exploramos sus vecinos
            for action in grid.actions(nodo_estudio.state):
                
                # Calculamos el nuevo estado después de la acción
                nuevo_estado = grid.result(nodo_estudio.state, action)

                # Solo avanzamos si este estado nunca fue visitado
                if nuevo_estado not in reached:
                    # Calculamos el costo
                    costo_mov = grid.individual_cost(nodo_estudio.state, action)
                    nuevo_costo = nodo_estudio.cost + costo_mov

                    # Marcamos como alcanzado
                    reached[nuevo_estado] = nuevo_costo
                    
                    # Creamos el nodo hijo
                    nodo_hijo = Node("", state=nuevo_estado, cost=nuevo_costo, parent=nodo_estudio, action=action)

                    # Lo añadimos al tope de la pila para explorarlo después
                    frontera.add(nodo_hijo)

        # Si la pila se vacía y no encontramos solución, devolvemos NoSolution
        return NoSolution(reached)
