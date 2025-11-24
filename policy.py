import numpy as np
from connect4.policy import Policy
import random
import math
import time

class GAMPolicy(Policy):

    def mount(self, time_out: int = 1):
        # Gradescope nos envía el tiempo máximo por jugada
        self.time_out = time_out

        # Online policy improvement:
        # guardamos stats por estado RAÍZ (no todo el árbol porque explota)
        # key = (hash_estado, col)
        # value = {"visitas": int, "ganadas": float}
        self.root_stats = {}

        # constante UCB
        self.c_ucb = 1.4

        # profundidad corta para simulación rápida
        self.rollout_depth = 18

    def act(self, board: np.ndarray) -> int:

        # Si mount() no fue llamado, creamos el atributo por defecto
        if not hasattr(self, "time_out"):
            self.time_out = 1

        if not hasattr(self, "root_stats"):
            self.root_stats = {}

        if not hasattr(self, "rollout_depth"):
            self.rollout_depth = 18

        if not hasattr(self, "c_ucb"):
            self.c_ucb = 1.4
                

        # convertir tablero a string (hash del estado)
        def hash_board(b):
            # más rápido que str(list)
            return tuple(b.reshape(-1))

        # obtener movimientos válidos
        # Los movimientos validos es una columna
        # cuya fila superios esta vacia
        def valid_moves(b):
            return [c for c in range(7) if b[0][c] == 0]

        # aplicar un movimiento
        def play(b, col, player):
            newb = np.array(b)
            for r in range(5, -1, -1):
                if newb[r][col] == 0: #Buscar la primera fila vacio en esa columna para poner la ficha
                    # Colocamos la ficha del jugador
                    newb[r][col] = player
                    break #Sale del bucle y retorna el nuevo tablero con la jugada aplicada
            return newb

        # evaluar ganador
        def winner(b):
            return self.checkWinner(b)

        """# crear nodo si no existe
        def ensure_node(b):
            hb = hash_board(b) #S0, S1, S2, ....
            if hb not in tree:
                tree[hb] = {
                    "visitas": 0,
                    "ganadas": 0.0,
                    "hijos": {}  # col -> next_state
                }
            return tree[hb] """
        

     
            
        #Online Policy Improvement con MCTS ligero SOLO EN RAÍZ
        hb_root = hash_board(board)
        

        def ensure_root_stat(col):
            key = (hb_root, col)
            if key not in self.root_stats:
                self.root_stats[key] = {"visitas": 0, "ganadas": 0.0}
            return self.root_stats[key]

        # UCB a nivel raíz
        def ucb_root(col, total_visits):
            st = ensure_root_stat(col)
            if st["visitas"] == 0:
                return 999999
            return (st["ganadas"] / st["visitas"]) + self.c_ucb * math.sqrt(
                math.log(total_visits + 1) / st["visitas"]
            )
        
        """
        # selección con UCB  -
        def ucb(node, parent_visits):
            if node["visitas"] == 0:
                return 999999  # para explorar primero
            return (node["ganadas"] / node["visitas"]) + 1.4 * math.sqrt(
                math.log(parent_visits + 1) / node["visitas"]
            )
            """

        # Simulation
        def simulation(b, player):
            for i in range(self.rollout_depth):
                w = winner(b)
                # Si ya hay un ganador
                if w != 0:
                   # Asigna su respectiva recompensa
                    if w == mi_jugador:
                        return 1
                    else:
                        return 0

                movs = valid_moves(b)
                if len(movs) == 0:
                    return 0.5  # empate

                c = random.choice(movs)
                b = play(b, c, player)
                player = -player
          # Termina el for
            return 0.5
        
        # total de visitas de todos los movimientos en raíz
        def total_root_visits():
            s = 0
            for c in movs_root:
                s += ensure_root_stat(c)["visitas"]
            return s

        # loop de mejora online mientras haya tiempo
        while time.time() < deadline:
            total_vis = total_root_visits()

            # escoger mejor movimiento por UCB
            mejor_col = None
            mejor_val = -999999
            for c in movs_root:
                val = ucb_root(c, total_vis)
                if val > mejor_val:
                    mejor_val = val
                    mejor_col = c

            # simular desde ese hijo
            b2 = play(board, mejor_col, mi_jugador)
            r = simulation(b2, -mi_jugador)

            # backprop SOLO a raíz (online improvement)
            st = ensure_root_stat(mejor_col)
            st["visitas"] += 1
            st["ganadas"] += r


        # elegir mejor movimiento final: más visitas
        mejor = None
        mejor_visitas = -1
        for c in movs_root:
            st = ensure_root_stat(c)
            if st["visitas"] > mejor_visitas:
                mejor_visitas = st["visitas"]
                mejor = c

        if mejor is None:
            mejor = random.choice(movs_root)

        return mejor

   #Verificación buscando cuatro fichas seguidas para saber si es un estado terminal
    def checkWinner(self, b):
        # horizontal
        for r in range(6):
            for c in range(4):
                v = b[r][c]
                if v != 0 and v == b[r][c+1] == b[r][c+2] == b[r][c+3]:
                    return v
        # vertical
        for r in range(3):
            for c in range(7):
                v = b[r][c]
                if v != 0 and v == b[r+1][c] == b[r+2][c] == b[r+3][c]:
                    return v
        # diagonal
        for r in range(3):
            for c in range(4):
                v = b[r][c]
                if v!=0 and v==b[r+1][c+1]==b[r+2][c+2]==b[r+3][c+3]:
                    return v
        # diagonal
        for r in range(3,6):
            for c in range(4):
                v = b[r][c]
                if v!=0 and v==b[r-1][c+1]==b[r-2][c+2]==b[r-3][c+3]:
                    return v
        return 0