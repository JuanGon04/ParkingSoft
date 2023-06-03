import cv2
import base64
import pytesseract

def ReconocimientoPlaca(file_path):
    # Leer la imagen
    image = cv2.imread(file_path)

    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar un filtro de desenfoque para reducir el ruido
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Aplicar un umbral adaptativo para binarizar la imagen
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 17, 1)

    # Encontrar contornos en la imagen binarizada
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Ordenar los contornos por área de mayor a menor
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    plate_text = ""
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)
        plate_area = w * h
        if 2 <= aspect_ratio <= 3 and 0.1 <= h / image.shape[0] <= 0.2 and 0.02 <= plate_area / (
                image.shape[0] * image.shape[1]) <= 0.1:
            plate_roi = gray[y:y + h, x:x + w]

            plate_text = pytesseract.image_to_string(
                plate_roi,
                config='--psm 7 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            )

            plate_text = ''.join(e for e in plate_text if e.isalnum())

            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 5)

            break





    # Generar representación base64 de la imagen en escala de grises
    _, encoded_gray = cv2.imencode('.png', image)
    ImagenMarco = base64.b64encode(encoded_gray).decode('utf-8')



    resultado = plate_text if plate_text else "No se encontró ninguna placa"

    return resultado, ImagenMarco