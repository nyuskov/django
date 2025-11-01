from .models import Order


def order(request):
    return {"order": Order(request)}
