#Brian's Brain
#José Manuel Quesada y Christopher Jiménez

############################# Imports #############################
import pygame as p
import json
from random import randrange
from copy import deepcopy
############################# Global Var #############################

_ANCHO = 1000
_ALTO = 800
_TAM = 7

_COLS = _ANCHO // _TAM + 1
_FILAS = _ALTO // _TAM + 1

############################# Matrices #############################

def crearMatrizRandom(filas, columnas, estados):
    """
    Función que crea una matriz con las dimensiones indicadas
    y con valores aleatorios en el rango de 3 estados (vivo, muriendo, muerto).
    Entradas y restricciones:
    - filas : cantidad de filas, número entero positivo.
    - columnas : cantidad de columnas, numero entero positivo.
    - estados : cantidad de estados, numero entero positivo.
    Salida:
    - Retorna la matriz (en forma de lista) con número de filas y columnas
    indicados, con celdas con estados aleatorios dentro del rango dado.
    """
    M = []
    for f in range(filas):
        fila = []
        for c in range(columnas):
            fila.append(randrange(estados))
        M.append(fila)
    return M

def crearMatriz(filas, columnas, valor):
    """
    Función que crea una matriz con las dimensiones indicadas
    y con el mismo valor en todas las celdas.
    Entradas y restricciones:
    - filas : cantidad de filas, número entero positivo.
    - columnas : cantidad de columnas, numero entero positivo.
    - valor : numero que tendrá cada celda de la matriz, entero positivo.
    Salida:
    - Retorna la matriz (en forma de lista) con número de filas y columnas
    indicados, con celdas que tienen el valor dado.
    """
    M = []
    for f in range(filas):
        fila = []
        for c in range(columnas):
            fila.append(valor)
        M.append(fila)
    return M

def imprimir(M):
    """
    Función que recibe una matriz y la imprime en pantalla.
    Entradas y restricciones:
    - M : matriz, creada a partir de una lista no vacía.
    Salida:
    - Matriz impresa en consola.
    """
    for fila in M:
        for valor in fila:
            print(valor, end="\t")
        print()

def brianCrearRandom():
    """
    Función encargada de crear la matriz random.
    Entradas y restricciones:
    - Ninguna.
    Salida:
    - Retorna la matriz que genera la función crearMatrizRandom.
    """
    return crearMatrizRandom(_FILAS, _COLS, 3)

def brianCrearLimpia():
    """
    Función encargada de crear la matriz limpia (con valores neutros).
    Entradas y restricciones:
    - Ninguna.
    Salida:
    - Retorna la matriz que genera la función crearMatriz.
    """
    return crearMatriz(_FILAS, _COLS, 0)


############################# Siguiente generación #############################

def brianNext(M):
    """
    Función que calcula la siguiente generación de una matriz
    según las reglas del autómata "Cerebro de Brian".
    Entradas y restricciones:
    - M : matriz, creada a partir de una lista no vacía.
    Salida:
    - Retorna la nueva matriz con la siguiente generación.
    """
    nuevaM = deepcopy(M)
    for f in range(len(M)):
        for c in range(len(M[0])):
            vec = vecinos(M, f, c)
            if M[f][c] == 0 and vec.count(1) == 2:
                nuevaM[f][c] = 1
            elif M[f][c] == 1:
                nuevaM[f][c] = 2
            elif M[f][c] == 2:
                nuevaM[f][c] = 0
    return nuevaM

def vecinos(M, fila, col):
    """
    Función que retorna una lista con los vecinos de la célula.
    Entradas y restricciones:
    - M : matriz, creada a partir de una lista no vacía.
    - fila : filas, número entero positivo.
    - col : columnas, numero entero positivo.
    Salida:
    - Retorna la lista de vecinos de la célula.
    """
    vec = []
    for f in range(fila - 1, fila + 2):
        for c in  range(col - 1, col + 2):
            if f != fila or c != col:
                vec.append(M[f % len(M)][c % len(M[0])])
    return vec

############################# Estado siguiente #############################

def brianSiguiente(estado):
    """
    Función que devuelve el otro estado de la celula.
    (El siguiente estado de la célula.)
    Entradas y restricciones:
    - estado : estado actual de la célula, número entero entre 0 y 2.
    Salida:
    - Retorna el siguiente estado de la célula.
    """

    return (estado + 1) % 3

############################# Dibujo en ventana #############################

def brianDibujar(M, window):
    """
    Función que se encarga de dibujar la matriz en la superficie
    window de pygame.
    Entradas y restricciones:
    - M : matriz, creada a partir de una lista no vacía.
    - window : superficie donde se va a mostrar la matriz.
    Salida:
    - Matriz dibujada en la ventana de pygame. 
    """
    for f in range(len(M)):
        for c in range(len(M[0])):
            if M[f][c] == 1:
                color = (230, 0, 153)
                rec = (c * _TAM, f * _TAM, _TAM, _TAM)
                p.draw.rect(window, color, rec)
            if M[f][c] == 2:
                color = (127,0,153)
                rec = (c * _TAM, f * _TAM, _TAM, _TAM)
                p.draw.rect(window, color, rec)


############################# Archivos #############################

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
    archivo = open("..\\archivos\\matrizBrian.txt", "w")
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
    archivo = open("..\\archivos\\matrizBrian.txt", "r")
    M = json.load(archivo)
    archivo.close()
    print("Estado cargado exitosamente")
    return M
    
############################# Main #############################

def main():
    """
    Función principal del Autómata Celular "Brian's Brain"
    Creado por medio de la biblioteca pygame.
    Entradas y restricciones:
    - Ninguna.
    Salida:
    - Autómata celular "Brian's Brain".
    """
    p.init()
    window = p.display.set_mode((_ANCHO, _ALTO))
    loop = True
    M = brianCrearRandom()
    pause = False
    while loop:
        p.time.delay(16)
        for event in p.event.get():
            if event.type == p.QUIT:
                loop = False
            if event.type == p.KEYDOWN:
                keys = p.key.get_pressed()
                if keys[p.K_SPACE]:
                    pause = not pause
                if keys[p.K_r]:
                    M = brianCrearRandom()
                if keys[p.K_b]:
                    M = brianCrearLimpia()
                if keys[p.K_g]:
                    guardarEstado(M)
                if keys[p.K_c]:
                    M = cargarEstado()
            if event.type == p.MOUSEBUTTONDOWN:
                x, y = p.mouse.get_pos()
                c = x // _TAM
                f = y // _TAM
                M[f][c] = brianSiguiente(M[f][c])
                
                    
        window.fill((0, 0, 0))
        brianDibujar(M, window)
        p.display.update()
        if not pause:
            M = brianNext(M)
            
    p.quit()

if __name__ == "__main__":
    main()
