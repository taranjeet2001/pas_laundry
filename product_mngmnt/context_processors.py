from product_mngmnt.models import Product


def brand_menu(request):
    raw_brands = (
        Product.objects.exclude(brand__isnull=True)
        .exclude(brand__exact="")
        .values_list("brand", flat=True)
    )

    brands = []
    seen = set()

    for brand in raw_brands:
        normalized = " ".join(brand.split())
        key = normalized.casefold()
        if key and key not in seen:
            seen.add(key)
            brands.append(normalized)

    brands.sort(key=str.casefold)
    return {"brand_menu": brands}
