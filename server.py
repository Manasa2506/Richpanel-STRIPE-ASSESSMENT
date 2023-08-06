
import os
from flask import Flask, redirect, jsonify, json, request, current_app

import stripe
# This is your test secret API key.
stripe.api_key = 'sk_test_51NbllzSHPUgNmFMxpQe6OabFmirbCu3bECbj3jiPIPFXsYcJesqkc2K2UvJZ01qI5qFO38ltIQ8fqcInrjwHniyO00juHmVRsk'

app = Flask(__name__,
            static_url_path='',
            static_folder='public')

YOUR_DOMAIN = 'http://localhost:4242'
app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        prices = stripe.Price.list(
            lookup_keys=[request.form['lookup_key']],
            expand=['data.product']
        )

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1NbxoMSHPUgNmFMxE9ml6Omh',
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=YOUR_DOMAIN +
            '/success.html?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
        # return redirect(checkout_session.url, code=303)
    except Exception as e:
        print(e)
    # return "Server error", 500
    return redirect(checkout_session.url, code=303)


# @app.route('/create-portal-session', methods=['POST'])
# def customer_portal():
#     # For demonstration purposes, we're using the Checkout session to retrieve the customer ID.
#     # Typically this is stored alongside the authenticated user in your database.
#     checkout_session_id = request.form.get('session_id')
#     checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)

#     # This is the URL to which the customer will be redirected after they are
#     # done managing their billing with the portal.
#     return_url = YOUR_DOMAIN

#     portalSession = stripe.billing_portal.Session.create(
#         customer=checkout_session.customer,
#         return_url=return_url,
#     )
#     return redirect(portalSession.url, code=303)


# @app.route('/webhook', methods=['POST'])
# def webhook_received():
#     # Replace this endpoint secret with your endpoint's unique secret
#     # If you are testing with the CLI, find the secret by running 'stripe listen'
#     # If you are using an endpoint defined with the API or dashboard, look in your webhook settings
#     # at https://dashboard.stripe.com/webhooks
#     webhook_secret = 'whsec_48a5a53756050651aa5246c7241e0d7306edc2e77436f08a37b467da36ae2ed9'
#     request_data = json.loads(request.data)

#     if webhook_secret:
#         # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
#         signature = request.headers.get('stripe-signature')
#         try:
#             event = stripe.Webhook.construct_event(
#                 payload=request.data, sig_header=signature, secret=webhook_secret)
#             data = event['data']
#         except Exception as e:
#             return e
#         # Get the type of webhook event sent - used to check the status of PaymentIntents.
#         event_type = event['type']
#     else:
#         data = request_data['data']
#         event_type = request_data['type']
#     data_object = data['object']

#     print('event ' + event_type)

#     if event_type == 'checkout.session.completed':
#         print('🔔 Payment succeeded!')
#     elif event_type == 'customer.subscription.trial_will_end':
#         print('Subscription trial will end')
#     elif event_type == 'customer.subscription.created':
#         print('Subscription created %s', event.id)
#     elif event_type == 'customer.subscription.updated':
#         print('Subscription created %s', event.id)
#     elif event_type == 'customer.subscription.deleted':
#         # handle subscription canceled automatically based
#         # upon your subscription settings. Or if the user cancels it.
#         print('Subscription canceled: %s', event.id)

#     return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(port=4242)
