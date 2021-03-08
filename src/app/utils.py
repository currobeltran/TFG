def estaRegistrado(request):
    if request.user.is_authenticated:
        return True
    else:
        return False
