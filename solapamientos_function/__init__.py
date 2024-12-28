# desarrollo de la funcion para detectar el solapamiento de eventos
# Detecta si un nuevo evento se solapa con una lista de eventos existentes.
# Si hay solapamiento, imprime un mensaje indicando el evento conflictivo.


def detectarSolapamientos(eventos, nuevo_evento):
        
    for evento in eventos:
        # Convertir horarios a minutos para facilitar las comparaciones
        inicio_existente = convertir_a_minutos(evento['inicio'])
        fin_existente = convertir_a_minutos(evento['fin'])
        inicio_nuevo = convertir_a_minutos(nuevo_evento['inicio'])
        fin_nuevo = convertir_a_minutos(nuevo_evento['fin'])

        # Comprobar solapamiento
        if inicio_nuevo < fin_existente and fin_nuevo > inicio_existente:
            print(f"Solapamiento detectado: Nuevo evento ({nuevo_evento['inicio']} - {nuevo_evento['fin']}) "
                  f"conflicta con evento existente ({evento['inicio']} - {evento['fin']}).")
            return True  # Hay solapamiento
    return False  # No hay solapamiento


def convertir_a_minutos(hora):
    #Convierte una hora en formato HH:MM a minutos desde la medianoche.
    #:param hora: Hora en formato 'HH:MM'.
    #:return: Minutos desde la medianoche.
    
    horas, minutos = map(int, hora.split(':'))
    return horas * 60 + minutos