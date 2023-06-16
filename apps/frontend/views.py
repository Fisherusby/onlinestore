import braintree
from django.conf import settings
from django.shortcuts import redirect, render
from tools.add_rnd import (
    create_brands_and_vendors,
    create_random_goods,
    create_vendors_and_offers,
)

from apps.info.tools import update_covid, update_currency


def index(request):
    return render(request, "index.html")


def updates_info(request):
    update_currency()
    update_covid()
    return redirect("index")


def add_cat_onliner(request, code_add):
    if code_add == 65535:
        # create_cat()
        create_brands_and_vendors()
        create_random_goods(70)
        create_vendors_and_offers(1, 5)
    return redirect("index")


# instantiate Braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def payment_process(request, order_id):
    total_cost = 1
    if request.method == "POST":
        # retrieve nonce
        nonce = request.POST.get("payment_method_nonce", None)
        # create and submit transaction

        result = gateway.transaction.sale(
            {
                "amount": f"{total_cost:.2f}",
                "payment_method_nonce": nonce,
                "options": {"submit_for_settlement": True},
            }
        )
        if result.is_success:
            # mark the order as paid
            # order.paid = True
            # # store the unique transaction id
            # order.braintree_id = result.transaction.id
            # order.save()
            return redirect("payment:done")
        else:
            return redirect("payment:canceled")
    else:
        # generate token
        client_token = gateway.client_token.generate()
        return render(
            request,
            "payment/process.html",
            {"order_id": order_id, "client_token": client_token},
        )


def payment_done(request):
    return render(request, "payment/done.html")


def payment_canceled(request):
    return render(request, "payment/canceled.html")
