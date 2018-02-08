from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter

from app.api.consumers import SubscriptionConsumer


application = ProtocolTypeRouter({
    'websocket': URLRouter([
        url('subscriptions', SubscriptionConsumer),
    ])
})
