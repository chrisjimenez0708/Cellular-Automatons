#Langton's Ant
#José Manuel Quesada y Christopher Jiménez

############################# Imports #############################
import pygame as p
import json
from random import randrange
from copy import deepcopy
############################# Global Var #############################

_ANCHO = 1000
_ALTO = 1000
_TAM = 5

_COLS = _ANCHO // _TAM + 1
_FILAS = _ALTO // _TAM + 1

hormiga = {
    "fila" : (_FILAS // 2) % (_FILAS + 1),
    "columna" : (_COLS // 2) % (_COLS + 1),
    "dir" : 0
    }

############################# Matrices #############################

def crearMatrizRandom(filas, columnas, estados):
    """
    Función que crea una matriz con las dimensiones indicadas
    y con valores aleatorios en el rango de 2 estados (blanco, negro).
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

def hormigaNext(M):
    """
    Función que se encarga de crear la siguiente matriz segun la posición
    de la hormiga en la matriz.
    Entradas y restricciones:
    - M : matriz, creada a partir de una lista no vacía.
    Utiliza el diccionario global "Hormiga".
    Salida:
    - Retorna la nueva matriz.
    """
    for f in range(len(M)):
        for c in range(len(M[0])):
            if hormiga["fila"] == f and hormiga["columna"] == c:
                nuevaM = movimientoHormiga(M, f, c)
                return nuevaM


def langtonCrearRandom():
    """
    Función encargada de crear la matriz random.
    Entradas y restricciones:
    - Ninguna.
    Salida:
    - Retorna la matriz que genera la función crearMatrizRandom.
    """
    return crearMatrizRandom(_FILAS, _COLS, 2)

def langtonCrearLimpia():
    """
    Función encargada de crear la matriz limpia (con valores neutros).
    Entradas y restricciones:
    - Ninguna.
    Salida:
    - Retorna la matriz que genera la función crearMatriz.
    """
    return crearMatriz(_FILAS, _COLS, 0)

############################# Hormiga #############################

def rotarDerecha():
    """
    Función que se encarga de girar a la hormiga 90 grados a la derecha.
    Entradas y restricciones:
    - Ninguna. Utiliza la variable global hormiga.
    Salida:
    - La dirección de la hormiga girada 90 grados a la derecha.
    """
    if hormiga["dir"] == 0:
        hormiga["dir"] += 3
    else:
        hormiga["dir"] -= 1
        
def rotarIzquierda():
    """
    Función que se encarga de girar a la hormiga 90 grados a la izquierda.
    Entradas y restricciones:
    - Ninguna. Utiliza la variable global hormiga.
    Salida:
    - La dirección de la hormiga girada 90 grados a la izquierda.
    """

    hormiga["dir"] = (hormiga["dir"] + 1) % 4

def avanzar():
    """
    Función que hace a la hormiga avanzar una celula.
    Entradas y restricciones:
    - Ninguna. Utiliza la variable global hormiga.
    Salida:
    - La hormiga movida una casilla al frente según su dirección.
    """
    if hormiga["dir"] == 0:
        hormiga["columna"] = (hormiga["columna"] + 1) % _COLS

    if hormiga["dir"] == 1:
        hormiga["fila"] = (hormiga["fila"] - 1) % _FILAS

    if hormiga["dir"] == 2:
        hormiga["columna"] = (hormiga["columna"] - 1) % _COLS

    if hormiga["dir"] == 3:
        hormiga["fila"] = (hormiga["fila"] + 1) % _FILAS
        
def movimientoHormiga(M, f, c):
    """
    Función que se encarga de mover a la hormiga y crear la nueva matriz.
    Entradas y restricciones:
    - M : matriz, creada a partir de una lista no vacía.
    - f : número de fila, debe ser un número que esté en el rango del
    largo de las filas de la matriz.
    - c : número de columna, debe ser un número que esté en el rango del
    largo de las columnas de la matriz.
    Salidas:
    - Retorna la nueva matriz y actualiza los valores del diccionario
    global hormiga.
    """
    nuevaM = deepcopy(M)
    if M[f][c] == 1:
        rotarDerecha()
        nuevaM[f][c] = 0
    else:
        rotarIzquierda()
        nuevaM[f][c] = 1
    avanzar()
    return nuevaM


############################# Estado siguiente #############################

def langtonSiguiente(estado):
    """
    Función que devuelve el otro estado de la celula.
    (El siguiente estado de la célula.)
    Entradas y restricciones:
    - estado : estado actual de la célula, número entero entre 0 y 1.
    Salida:
    - Retorna el siguiente estado de la célula.
    """

    return (estado + 1) % 2

############################# Dibujo en ventana #############################

def langtonDibujar(M, window):
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
                color = (255, 255, 255)
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
    archivo = open("..\\archivos\\matrizLangton.txt", "w")
    json.dump(M, archivo)
    archivo.close()
    print("Estado guardado exitosamente.")

def cargarEstado():
    """
    Función que se encarga de cargar el estado del autómata.
    Entradas y restricciones:
    - Ninguna. La función es llamada cuando se presiona la tecla C.
    Salida:
    - Matriz obtenida del archivo. Adicionalmente, se imprime
    en consola que el estado fue cargado exitosamente.
    """
    archivo = open("..\\archivos\\matrizLangton.txt", "r")
    M = json.load(archivo)
    archivo.close()
    print("Estado cargado exitosamente.")
    return M

def guardarHormiga():
    """
    Función que se encarga de guardar las propiedades de la hormiga.
    Entradas y restricciones:
    - Ninguna. Utiliza el diccionario global "Hormiga".
    La función es llamada cuando se presiona la tecla G.
    Salida:
    - Archivo guardado en la carpeta archivos. Adicionalmente, imprime
    en consola que las propiedades fueron guardadas exitosamente.
    """
    archivo = open("..\\archivos\\hormigaLangton.txt", "w")
    json.dump(hormiga, archivo)
    archivo.close()
    print("Propiedades de la hormiga guardadas exitosamente.")

def cargarHormiga():
    """
    Función que se encarga de cargar las propiedades de la hormiga.
    Entradas y restricciones:
    - Ninguna. La función es llamada cuando se presiona la tecla C.
    Salida:
    - Diccionario de la hormiga obtenido del archivo. Adicionalmente, imprime
    en consola que las propiedades fueron cargadas exitosamente.
    """
    global hormiga
    archivo = open("..\\archivos\\hormigaLangton.txt", "r")
    hormiga = json.load(archivo)
    archivo.close()
    print("Propiedades de la hormiga cargadas exitosamente.")
    
############################# Main #############################

def main():
    """
    Función principal del Autómata Celular "Langton's Ant"
    Creado por medio de la biblioteca pygame.
    Entradas y restricciones:
    - Ninguna.
    Salida:
    - Autómata celular "Langton's Ant".
    """
    p.init()
    window = p.display.set_mode((_ANCHO, _ALTO))
    loop = True
    M = langtonCrearLimpia()
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
                    M = langtonCrearRandom()
                if keys[p.K_b]:
                    M = langtonCrearLimpia()
                    hormiga["fila"] = (_FILAS // 2) % (_FILAS + 1)
                    hormiga["columna"] = (_COLS // 2) % (_COLS + 1)
                    hormiga["dir"] = 0
                if keys[p.K_g]:
                    guardarEstado(M)
                    guardarHormiga()
                if keys[p.K_c]:
                    M = cargarEstado()
                    cargarHormiga()
            if event.type == p.MOUSEBUTTONDOWN:
                x, y = p.mouse.get_pos()
                c = x // _TAM
                f = y // _TAM
                M[f][c] = langtonSiguiente(M[f][c])
                
                    
        window.fill((0, 0, 0))
        langtonDibujar(M, window)
        p.display.update()
        if not pause:
            M = hormigaNext(M)
            
    p.quit()

if __name__ == "__main__":
    main()



