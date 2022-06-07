#Implementación del autómata celular cíclico.
#Christopher Jiménez y José Manuel Quesada. 

###################### IMPORTS ########################
import pygame
from random import randrange
from copy import deepcopy
import json

##################### VARIABLES GLOBALES #####################
_ANCHO = 1000
_ALTO = 700
_TAM = 9
_COLS = _ANCHO // _TAM + 1
_FILAS = _ALTO // _TAM + 1

####################### MATRICES #############################
def generarMatrizRandom(filas, cols, estados):
    """
    Función que crea una matriz con las filas y columnas dadas, con
    valores aleatorios entre 0 y estados - 1.
    Entradas y restricciones:
    filas: número de filas de la matriz, número entero positivo.
    columnas: número de columnas de la matriz, número entero positivo.
    Estados: cantidad de estados de la matriz, número entero positivo.
    Salida:
    Una lista, con listas que representan a la matriz.
    """
    M = []
    for f in range(filas):
        fila = []
        for c in range(cols):
            fila.append(randrange(estados))
        M.append(fila)
    return M

def generarMatriz(filas, cols, valor):
    """
    Función que crea una matriz con las dimensiones dadas,
    y con el valor recibido en todas las celdas.
    Entradas y restricciones:
    - filas: número de filas de la matriz, entero positivo.
    - columnas: número de columnas de la matriz, entero positivo.
    - valor: valor que se añadirá a todas las celdas.
    Salida:
    Una lista con listas, que representa la matriz.
    """
    M = []
    for f in range(filas):
        fila = []
        for c in range(cols):
            fila.append(valor)
        M.append(fila)
    return M
    
def vecinos(M, fila, col):
    """
    Función que retorna una lista con los vecinos de
    una celda del autónoma.
    Entradas y restricciones:
    M: una matriz.
    fila: fila de la celda, entero no negativo.
    columna: columna de la celda: entero no negativo.
    Salida:
    lista con los vecinos de la celda. 
    """
    vec = []
    for f in range(fila - 1, fila + 2):
        for c in range(col - 1, col + 2):
            if f != fila or c != col:
                vec.append(M[f % len(M)][c % len(M[0])])
    return vec

def nextGeneration(M):
    """
    Función que recibe la matriz del autómata y devuelve la siguiente generación de
    las celdas según las reglas del autómata celular cíclico. 
    Entradas y restricciones:
    M: una matriz.
    Salida:
    siguiente generación con valores actualizados de las celdas. 
    """
    newM = deepcopy(M)
    for f in range(len(list(M))):
        for c in range(len(M[0])):
            vec = vecinos(M, f, c)
            for v in vec:
                if v == nexState(M[f][c]):
                    newM[f][c] = nexState(M[f][c])
    return newM
                    
def nexState(cel):
    """
    Función que recibe una valor de una celda del autómata y devuelve su siguiente estado.
    Entradas y restricciones.
    cel: un valor en una celda
    Salida:
    el siguiente valor de la celda
    """
    return (cel + 1) % 16

#################### DIBUJO EN VENTANA #######################
def draw(M, window):
    colors = [(255, 0, 0), (245, 57, 7), (244, 164, 23), (249, 233, 37), (136, 249, 37), (42, 236, 26), (84, 231, 111), (42, 249, 158),(31, 246, 207), (40, 183, 225), (13, 114, 144), (13, 35, 144), (144, 49, 195), (234, 28, 234), (247, 26, 187), (247, 26, 126)]
    for f in range(len(list(M))):
        for c in range(len(M[0])):
            color = colors[M[f][c]]
            rec = (c * _TAM, f * _TAM, _TAM, _TAM)
            pygame.draw.rect(window, color, rec)
            
############################# ARCHIVOS #############################
def guardarEstado(M):
    """
    Función que se encarga de guardar el estado del autómata.
    Entradas y restricciones:
    - M : matriz, creada a partir de una lista no vacía.
    La función es llamada cuando se presiona la tecla G.
    Salida:
    - Archivo guardado en la carpeta archivos. Adicionalmente, imprime
    en consola que el estado fue guardado exitosamente.
    """
    archivo = open("..\\archivos\\matrizCelularCiclico.txt", "w")
    json.dump(M, archivo)
    print("Estado guardado exitosamente")
    archivo.close()

def cargarEstado():
    """
    Función que se encarga de cargar el estado del autómata.
    Entradas y restricciones:
    - Ninguna. La función es llamada cuando se presiona la tecla C.
    Salida:
    - Matriz obtenida del archivo. Adicionalmente, se imprime
    en consola que el estado fue cargado exitosamente.
    """
    archivo = open("..\\archivos\\matrizCelularCiclico.txt", "r")
    M = json.load(archivo)
    archivo.close()
    print("Estado cargado exitosamente")
    return M


def main():
    """
    Función principal del programa que ejecuta el autónoma celular cíclico.
    """
    pygame.init()
    window = pygame.display.set_mode((_ANCHO, _ALTO))
    loop = True
    pause = False
    M = generarMatrizRandom(_FILAS, _COLS, 16)
    while loop:
        pygame.time.delay(16)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    pause = not pause
                if keys[pygame.K_r]:
                    M = generarMatrizRandom(_FILAS, _COLS, 16)
                if keys[pygame.K_b]:
                    M = generarMatriz(_FILAS, _COLS, 0)
                if keys[pygame.K_g]:
                    guardarEstado(M)
                if keys[pygame.K_c]:
                    M = cargarEstado()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                c = x // _TAM
                f = y // _TAM
                M[f][c] = nexState(M[f][c])

                    
        window.fill((0, 0, 0))
        draw(M, window)
        pygame.display.update()
        if not pause:
            M = nextGeneration(M)
    pygame.quit()

if __name__ == "__main__":
    main()












                

    

