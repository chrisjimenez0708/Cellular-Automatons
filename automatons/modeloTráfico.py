#Implementación del autómata Modelo de tráfico Biham-Middleton-Levine
#Programa creado por Christopher Jiménez y José Manuel Quesada. 


########################## IMPORTS ########################################
import pygame
from random import choice
from copy import deepcopy
import json


######################## VARIABLES GLOBALES ###############################
_ANCHO = 800 
_ALTO = 500
_TAM = 4
_COLS = _ANCHO // _TAM + 1
_FILAS = _ALTO // _TAM + 1

######################### MATRICES #######################################

def generarMatrizRandom(filas, cols):
    """
    Función que crea una matriz para el autómata con las filas y columnas dadas, con
    valores aleatorios entre 0 y 2.
    Entradas y restricciones:
    filas: número de filas de la matriz, número entero positivo.
    columnas: número de columnas de la matriz, número entero positivo.
    Salida:
    Una lista, con listas que representan a la matriz.
    """
    M = []
    for f in range(filas):
        fila = []
        for c in range(cols):
            fila.append(choice([0, 0, 0, 1, 2]))
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
    
def nextBlueGeneration(M):
    """
    Función que recibe la matriz del autómata y devuelve la siguiente generación de
    las celdas azules.
    Entradas y restricciones:
    M: una matriz.
    Salida:
    siguiente generación de las celdas azules.
    """
    
    newM = deepcopy(M)
    for f in range(len(M)):
        for c in range(len(M[0])):
            if M[f][c] == 1:
                if M[(f + 1) % _FILAS][c] == 0:
                    newM[f][c] = 0
                    newM[(f + 1) % _FILAS][c] = 1
    return newM

def nextRedGeneration(M):
    """
    Función que recibe la matriz del autómata y devuelve la siguiente generación de
    las celdas rojas.
    Entradas y restricciones:
    M: una matriz.
    Salida:
    siguiente generación de las celdas rojas.
    """
    newM = deepcopy(M)
    for f in range(len(M)):
        for c in range(len(M[0])):
            if M[f][c] == 2:
                if M[f][(c + 1) % _COLS] == 0:
                    newM[f][c] = 0
                    newM[f][(c + 1) % _COLS] = 2         
    return newM

def nexState(cel):
    """
    Función que recibe una valor de una celda del autómata y devuelve su siguiente estado.
    Entradas y restricciones.
    cel: un valor en una celda
    Salida:
    el siguiente valor de la celda
    """
    return (cel + 1) % 3


######################## DIBUJO EN VENTANA ###################################
def draw(M, window):
    """
    Función que dibuja una matriz en una ventana, con los colores del
    autómata Modelo de tráfico Biham-Middleton-Levine
    Entradas y restricciones:
    M: una matriz.
    window: una ventana para dibujar.
    Salida:
    la matriz dibujada en la ventana.
    """
    colors = [(255, 255, 255), (0, 0, 255), (255, 0, 0)]
    for f in range(len(M)):
        for c in range(len(M[0])):
            color = colors[M[f][c]]
            rec = (c*_TAM, f * _TAM, _TAM, _TAM)
            pygame.draw.rect(window, color, rec)


############################# ARCHIVOS ################################

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
    archivo = open("..\\archivos\\matrizTransito.txt", "w")
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
    archivo = open("..\\archivos\\matrizTransito.txt", "r")
    M = json.load(archivo)
    archivo.close()
    print("Estado cargado exitosamente")
    return M

########################## MAIN ############################

             
def main():
    """
    Función principal del programa que ejecuta el autómata Modelo de tráfico Biham-Middleton-Levine
    """
    pygame.init()
    window = pygame.display.set_mode((_ANCHO, _ALTO))
    loop = True
    pause = False
    M = generarMatrizRandom(_FILAS, _COLS)
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
                    M = generarMatrizRandom(_FILAS, _COLS)
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

        window.fill((255, 255, 255))
        draw(M, window)
        pygame.display.update()
        if not pause:
            M = nextBlueGeneration(M)
            M = nextRedGeneration(M)


    pygame.quit()



if __name__ == "__main__":
    main()
        
    





                        
