from django.shortcuts import render
from .models import Product
from auction.models import PositionAuction
from numpy import random


def index(request):
    """View function for the main product listing page.

    Returns:
        HttpResponse-object with rendered text (via 'render')
    """
    # Retrieve products from database
    product_list = Product.objects.values()

    # determine primitive parameters for the auction game, including valuation draws
    # note: identity of bidder corresponds to a product
    valuations = list(zip(range(1, 16), random.normal(25, 8, 15)))
    ctrs = [0.2, 0.17, 0.14, 0.12, 0.10, 0.08]
    slots = 6

    # create new auction instance and compute equilibrium bids
    auction = PositionAuction(slots, valuations, ctrs)
    auction_result = auction.compute_equilibrium()

    # enrich list of products with auction results
    for product, bid  in zip(product_list, auction_result['bids']):
        product['bid'] = bid[1]

    # prepare the context for the view to be rendered
    context = {
        'product_list': product_list,
        'available_slots': slots,
        'valuations': sorted(zip(product_list, [x[1] for x in valuations]), key=lambda x: x[0]['bid'], reverse=True),
        'revenue': auction_result['expected revenue'],
        'ctrs': ctrs
    }

    return render(request, 'products/index.html', context)