import sensor, image, time

# 1. Configuración inicial
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_exposure(False, exposure_us=20000)
sensor.set_saturation(3)
sensor.set_contrast(3)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

clock = time.clock()

# 2. Definir los umbrales para cada color (¡Usa tu script calibrador para ajustarlos!)
# Ejemplo: Valores aproximados para Rojo y Azul
#mean_rojo = ()
threshold_rojo = (25, 64, 36, 80, 13, 66)
threshold_verde = (17, 67, -45, -21, 3, 37)

# 3. Agrupamos los umbrales en una lista
# El orden es importante para el blob.code()
# Índice 0 (Rojo) = Código 1
# Índice 1 (Azul) = Código 2
thresholds = [threshold_rojo, threshold_verde]

while(True):
    clock.tick()
    img = sensor.snapshot()

    # Pasamos la lista 'thresholds' completa
    blobs = img.find_blobs(thresholds,
                           pixels_threshold=30,
                           area_threshold=30,
                           merge=True,
                           x_stride=2,
                           y_stride=2)

    if blobs:
        # Ya no buscamos solo el más grande, iteramos sobre todos los encontrados
        for blob in blobs:

            # 4. Identificar qué color es usando blob.code()
            if blob.code() == 1: # Código 1 corresponde al primer elemento (Rojo)

                img.draw_rectangle(blob.rect(), color=(255, 0, 0), thickness=2)
                img.draw_cross(blob.cx(), blob.cy(), color=(255, 0, 0))
                # Aquí podrías enviar la instrucción a tus subsistemas
                # print(f"Objetivo ROJO en X: {blob.cx()}")

            elif blob.code() == 2: # Código 2 corresponde al segundo elemento (Verde)

                img.draw_rectangle(blob.rect(), color=(60, 255, 0), thickness=2)
                img.draw_cross(blob.cx(), blob.cy(), color=(60, 255, 0))
                # print(f"Objetivo VERDE en X: {blob.cx()}")
