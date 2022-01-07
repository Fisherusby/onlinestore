import braintree
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings


def index(request):
    return render(request, 'index.html')


# instantiate Braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def payment_process(request):
    total_cost = 1
    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction

        import pdb
        pdb.set_trace()


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
            {'order': 111, 'client_token': client_token}
        )


def payment_done(request):
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')

