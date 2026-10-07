from django.db.models import Q
from product_mngmnt.models import Product


def _unique_brand_list(queryset):
    brands = []
    seen = set()

    for brand in queryset.values_list("brand", flat=True):
        normalized = " ".join((brand or "").split())
        key = normalized.casefold()
        if key and key not in seen:
            seen.add(key)
            brands.append(normalized)

    brands.sort(key=str.casefold)
    return brands


def brand_menu(request):
    parts_queryset = (
        Product.objects.filter(detail__icontains="part")
        .exclude(brand__isnull=True)
        .exclude(brand__exact="")
    )
    return {"brand_menu": _unique_brand_list(parts_queryset)}


def consumable_menu(request):
    consumables_queryset = (
        Product.objects.filter(
            Q(detail__icontains="consumable")
            | Q(detail__icontains="marking")
            | Q(detail__icontains="pads")
            | Q(detail__icontains="flat")
        )
        .exclude(brand__isnull=True)
        .exclude(brand__exact="")
    )
    return {"consumable_menu": _unique_brand_list(consumables_queryset)}
