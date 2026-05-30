# pyrefly: ignore [missing-import]
from django.db.models import Sum
from .models import CartItem


def cart_count(request):
    """
    Global context processor that injects `cart_count` into every template.
    This ensures the navbar cart badge always shows the correct number.
    """
    count = 0
    if request.user.is_authenticated:
        count = (
            CartItem.objects.filter(user=request.user)
            .aggregate(total=Sum('quantity'))['total'] or 0
        )
    return {'cart_count': count}
