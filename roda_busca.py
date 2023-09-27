""" 
Executa a busca em um mapa com custo fixo
"""

from busca_base import GridWithAdjustedWeights
from busca_largura import BuscaLargura
from busca_dijkstra import BuscaDijkstra
from busca_astar import BuscaAStar

MAP_NAME = "map.png"

def main():

    mapa = GridWithAdjustedWeights(MAP_NAME)

    busca = BuscaAStar()

    busca.do_search(mapa, start = (140,120), goal = (90, 80)) 


if __name__ == "__main__":
    main()

