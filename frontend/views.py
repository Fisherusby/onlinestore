import braintree
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

import tools.add_rnd
from info.tools import update_currency, update_covid
from tools.add_rnd import create_cat


def index(request):
    return render(request, 'index.html')


def updates_info(request):
    update_currency()
    update_covid()
    return redirect('index')

def add_cat_onliner(request, code_add):
    create_cat()
    return redirect('index')


# instantiate Braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def payment_process(request, order_id):
    total_cost = 1
    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction

        result = gateway.transaction.sale({
            'amount': f'{total_cost:.2f}',
            'payment_method_nonce': nonce,
            'options': {
            'submit_for_settlement': True
                }
            })
        if result.is_success:
            # mark the order as paid
            # order.paid = True
            # # store the unique transaction id
            # order.braintree_id = result.transaction.id
            # order.save()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:

        # generate token
        client_token = gateway.client_token.generate()
        return render(
            request,
            'payment/process.html',
            {'order_id': order_id, 'client_token': client_token}
        )


def payment_done(request):
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')

