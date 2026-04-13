from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class AStarSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using A* Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize root node
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)


        #Calculamos el f(n) = g(n) + h(n)
        #En este caso es 0 + la distancia hasta la meta (calculada con la distancia Manhattan)
        root.estimated_distance = root.cost + grid.heuristica(root.state)

        # Initialize reached with the initial state
        reached = {}
        reached[root.state] = root.cost

        # Initialize frontier with the root node
        frontera = PriorityQueueFrontier()
        frontera.add(root)


        #Mientras la cola NO este vacía, seguí explorando
        while not frontera.is_empty():

            #Sacamos al nodo con el MENOR valor de f(n)
            nodo_estudio = frontera.pop()

            #Si el nodo que estamos estudiando ES el objetivo, devolvemos la solución
            if grid.objective_test(nodo_estudio.state):
                return Solution(nodo_estudio, reached)
            
            #Si NO es la solución, seguimos
            #Vemos cuáles son las posibles acciones (arriba, abajo, etc)
            for action in grid.actions(nodo_estudio.state):
                #Calculamos en que coordenadas caería con esa accción
                nuevo_estado = grid.result(nodo_estudio.state, action)

                #calculamos el g(n) para llegar a esa baldosa
                costo_mov = grid.individual_cost(nodo_estudio.state, action)
                #Hacemos la suma del costo que veniamos acumulando y la acción que realizamos
                nuevo_costo = nodo_estudio.cost + costo_mov


                #Solo avanzamos acá, si esta baldosa nunca la pisamos, o si la pisamos pero hay un camino más barato
                if nuevo_estado not in reached or nuevo_costo < reached[nuevo_estado]:
                    #Actualizamos el valor del estado de esta nueva baldosa (con su valor más bajo)
                    reached[nuevo_estado] = nuevo_costo

                    #Nuevo Nodo Hijo
                    nodo_hijo = Node("", state= nuevo_estado, cost= nuevo_costo, parent= nodo_estudio, action= action)

                    #Le preguntamos al laberinto a que distancia quedo de la meta
                    h = grid.heuristica(nuevo_estado)
                    #Guardamos el f(n) total del nodo_hijo 
                    nodo_hijo.estimated_distance = nuevo_costo + h

                    #Lo mandamos a la cola, con su valor de prioridad
                    frontera.add(nodo_hijo, priority=nodo_hijo.estimated_distance)


        return NoSolution(reached)
