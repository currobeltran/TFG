# Función para comprobar si el usuario está registrado
def estaRegistrado(request):
    if request.user.is_authenticated:
        return True
    else:
        return False

# Función para formatear un año academico de la siguiente manera: 
# 20xx/20xx+1
def formatearAnio(añoString):
    año1 = añoString[0] + añoString[1] + añoString[2] + añoString[3]
    año2 = añoString[4] + añoString[5] + añoString[6] + añoString[7]
    
    return año1 + "/" + año2
