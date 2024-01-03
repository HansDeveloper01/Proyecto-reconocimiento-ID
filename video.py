# Librerías necesarias
import cv2
import pytesseract
import re

# Variables
encuadre = 100 # Necesitaremos ubicar el documento a identificar en un cuadro
documento = 0 # Documento a identificar (0 - 2)
                # 0 = nada, 1 = documento colombiano, 2 = otro documento

# Instnciamos la videocaptura que leerá el documento
captura = cv2.VideoCapture(0)
captura.set(3, 1280)
captura.set(4, 720)

def texto(imagen):
    global documento
    
    # Dirección pytesseract
    pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    # Gris
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Filtro
    umbral = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 55, 25)

    # Configuración OCR
    config = "--psm 1"
    text = pytesseract.image_to_string(umbral, config=config)

    # Palabras clave
    a = r"COLOMBIA"
    b = r"IDENTIFICACION"

    busqueda_1 = re.findall(a, text)
    busqueda_2 = re.findall(b, text)

    print(busqueda_1, busqueda_2)

    if len(busqueda_1) != 0 and len(busqueda_2) != 0:
        documento = 1

    print(text)

# Empezamos un While infinito que ejecutará el programa
while True:
    # lectura de la videocaptura
    ret, frame = captura.read()

    # Interfaz en pantalla
    cv2.putText(frame, "Ubique el documento", (180, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.71, (0, 0, 255), 2)
    cv2.rectangle(frame, (encuadre, encuadre), (600 - encuadre, 450 - encuadre), (0, 0, 255), 2)

    # Escenarios
    if documento == 0:
        cv2.putText(frame, "Presione 'S' para identificar", (150, 370), cv2.FONT_HERSHEY_SIMPLEX, 0.71, (0, 0, 255), 2)
    
    elif documento == 1:
        cv2.putText(frame, "IDENTIFICACION COLOMBIANA", (150, 370), cv2.FONT_HERSHEY_SIMPLEX, 0.71, (0, 255, 255), 2)

    # Lectura del teclado
    t = cv2.waitKey(5)
    cv2.imshow("ID", frame)

    # Escape
    if t == 27:
        break
    #
    elif t == 83 or t == 115:
        texto(frame)

captura.release
cv2.destroyAllWindows()