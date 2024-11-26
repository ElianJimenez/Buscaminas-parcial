from tkinter import *
from tkinter import messagebox
import random
import time
from PIL import Image, ImageTk  # Importamos Pillow (PIL) para manejar imágenes

# Configura la ventana
root = Tk()
root.title("Buscaminas")
root.iconbitmap("bombaico.png")  # Icono de la ventana (bombaico.png)
root.resizable(False, False)

frame = Frame(root, width=400, height=400)
frame.pack()

# Variables globales
bombasCerca = 0
win = False
listaBotones = []
reset = False
inicio = False
varSlotPulsado = -1
banderasDisponibles = 10
tiempoFin = 0
tiempoActual = 0
tiempoInicio = time.time()
bandera = False
tiempoHabilitado = False
tomarTiempoFin = 0
y = 0

# Contador de tiempo
contadorTiempo = Label(frame)
contadorTiempo.grid(column=1, row=0, columnspan=4)

# Función para mostrar el tiempo transcurrido
def tiempo(tiempo1=""):
    global tiempoInicio, tiempoActual, inicio, tomarTiempoFin, tiempoHabilitado, y, tiempo2
    tiempo2 = time.time()
    if tiempo1 != tiempo2 and tiempoHabilitado == True:
        tiempo1 = tiempo2
        tiempoActual = int(tiempo2 - tiempoInicio)
        contadorTiempo.config(text="Tiempo transcurrido: " + str(tiempoActual), font=("Arial 15"))
    else:
        tiempo1 = tiempo2
        y += 1
        if y == 1:
            tomarTiempoFin = int(tiempo2 - tiempoInicio)
            print("termino en: ", tomarTiempoFin)
        contadorTiempo.config(text="Tiempo transcurrido: " + str(tomarTiempoFin), font=("Arial 15"))
    contadorTiempo.after(200, tiempo)

# Función para generar los botones del tablero
def generarBotones():
    global listaBotones
    for c in range(81):
        listaBotones.append(Button(frame, width=6, height=3, text=" ", font=("Arial 12 bold"), command=lambda c=c: slotPulsado(c), bg="grey"))
        row = c // 9
        col = c % 9
        listaBotones[c].grid(column=col+1, row=row+1)
generarBotones()

# Función para generar las bombas en posiciones aleatorias
def bombasRandom():
    global bomba1, bomba2, bomba3, bomba4, bomba5, bomba6, bomba7, bomba8, bomba9, bomba10
    bombas = random.sample(range(81), 10)  # Genera 10 posiciones únicas aleatorias
    bomba1, bomba2, bomba3, bomba4, bomba5, bomba6, bomba7, bomba8, bomba9, bomba10 = bombas

bombasRandom()
print("Las ubicaciones de las bombas son: ", bomba1, bomba2, bomba3, bomba4, bomba5, bomba6, bomba7, bomba8, bomba9, bomba10)

# Cargar imagen con Pillow
def cargar_imagen(ruta):
    img = Image.open(ruta)  # Cargar la imagen
    img = img.resize((64, 65))  # Redimensionar la imagen (opcional)
    return ImageTk.PhotoImage(img)  # Convertirla a un formato que Tkinter puede manejar

# Cargar las imágenes
imagenBomba = cargar_imagen("bomba.png")
banderaImg = cargar_imagen("bandera.png")
banderaImgSlot = cargar_imagen("banderaSlot.png")
iconoBomba = cargar_imagen("bombaico.png")  # Icono de la ventana (también con Pillow)

# Función para mostrar las bombas cuando el jugador pierde
def mostrarBombas():
    for bomba in [bomba1, bomba2, bomba3, bomba4, bomba5, bomba6, bomba7, bomba8, bomba9, bomba10]:
        listaBotones[bomba].config(image=imagenBomba, width=64, height=65)

# Función que maneja el evento cuando un botón es presionado
def slotPulsado(slot):
    global bomba1, bomba2, bomba3, bomba4, bomba5, bomba6, bomba7, bomba8, bomba9, bomba10, listaBotones, bombasCerca, numeroPulsaciones, imagenBomba, win, reset, varSlotPulsado, inicio, ponerBandera, bandera, tiempoHabilitado, tomarTiempoFin, contadorTiempo, tiempoFin, tiempo2, tiempoInicio
    numeroPulsaciones = 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,
    bombasCerca = 0
    varSlotPulsado = slot
    tiempoHabilitado = True

    if not inicio:
        inicio = True
        tiempo()

    if win != True:
        if slot in [bomba1, bomba2, bomba3, bomba4, bomba5, bomba6, bomba7, bomba8, bomba9, bomba10]:
            if bandera == True:
                ponerBandera()
            else:
                mostrarBombas()
                listaBotones[slot].config(image=imagenBomba, width=64, height=65, bg="#f17070")
                tiempoHabilitado = False
                reset = messagebox.askyesno("Game Over", "¿Desea volver a jugar?")
                gameReset()
        else:
            def check():
                global bombasCerca
                for direction in [1, -1, 9, -9, 8, -8, 10, -10]:  # Direcciones alrededor de la casilla
                    if slot + direction in [bomba1, bomba2, bomba3, bomba4, bomba5, bomba6, bomba7, bomba8, bomba9, bomba10]:
                        bombasCerca += 1

            check()

            if bandera == False:
                listaBotones[slot].config(text=bombasCerca, fg="black", font=("Arial 12 bold"))
                listaBotones[slot].config(bg="#aeb0b2", state="disabled")
            else:
                ponerBandera()

            def checkWin():
                global imagenBomba, listaBotones, win, contadorBanderas
                if all(slot not in [bomba1, bomba2, bomba3, bomba4, bomba5, bomba6, bomba7, bomba8, bomba9, bomba10] for slot in range(81)) and numeroPulsaciones == 71:
                    win = True
                    txtWin1 = Label(frame, width=25, height=2, text="¡  G  A  N  A  S  T  E  !", font=("helvetica 27 bold"), bg="#fe4a4a")
                    txtWin1.grid(row=10, column=1, columnspan=9)
                    frame.config(bg="#fe4a4a")
                    contadorBanderas.config(bg="#fe4a4a")
                    contadorTiempo.config(bg="#fe4a4a")
                    mostrarBombas()
            checkWin()

# Función para presionar la bandera
def presionarBandera():
    global bandera
    bandera = True

# Función para colocar la bandera
def ponerBandera():
    global varSlotPulsado, bandera, banderasDisponibles, contadorBanderas, botonBandera, listaBotones
    if bandera and banderasDisponibles > 0:
        banderasDisponibles -= 1
        contadorBanderas.config(text="Banderas disponibles: " + str(banderasDisponibles))
        listaBotones[varSlotPulsado].config(image=banderaImgSlot, width=64, height=65)
        print("Bandera puesta en: ", varSlotPulsado)
    bandera = False

# Función para reiniciar el juego
def gameReset():
    global reset, bombasCerca, win, listaBotones, tiempoActual, tiempoInicio, tiempo1, tiempo2, tiempoActual, banderasDisponibles, bandera, y, tomarTiempoFin, tiempoHabilitado
    if reset == True:
        # Reiniciar todo el juego
        bombasCerca = 0
        win = False
        listaBotones = []
        bombasRandom()
        generarBotones()
        tiempoInicio = time.time()
        tiempo()
        banderasDisponibles = 10
        contadorBanderas.config(text="Banderas disponibles: " + str(banderasDisponibles))
        bandera = False
        reset = False
    else:
        root.destroy()

# Loop principal
root.mainloop()
