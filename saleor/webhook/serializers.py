from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    # pylint: disable=unused-import
    from ..checkout.models import Checkout


def serialize_checkout_lines(checkout: "Checkout") -> List[dict]:
    data = []
    channel = checkout.channel
    for line in checkout.lines.prefetch_related("variant__product").all():
        variant = line.variant
        product = variant.product
        data.append(
            {
                "sku": variant.sku,
                "quantity": line.quantity,
                "base_price": str(variant.get_price(channel.slug).amount),
                "currency": channel.currency_code,
                "full_name": variant.display_product(),
                "product_name": product.name,
                "variant_name": variant.name,
            }
        )
    return data
