

#Función para extraer los precios de forma segura
def extraer_precio(price_str, moneda):
    try:
        precios = eval(price_str) if isinstance(price_str, str) else {}  #Convierte string a diccionario
        valor = precios.get(moneda, None)  #Obtiene el valor de la moneda
        return float(valor) if valor not in [None, ""] else None  #Convierte a float si no es None o vacío
    except (SyntaxError, NameError, ValueError, TypeError):
        return None  #Si hay error, devuelve None