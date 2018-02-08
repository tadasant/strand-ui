from channels.generic.websocket import WebsocketConsumer


class SubscriptionConsumer(WebsocketConsumer):
    # TODO: Authenticate and potentially reject
    # TODO: Add user to group by user ID
    def connect(self):
        self.accept()
        print(self.channel_name)

    # TODO: Validate and store subscription in SubscriptionStore
    def receive(self, text_data=None, bytes_data=None):
        # Validate
        # Add to pubsub
        self.send(text_data=text_data)

    # TODO: Remove subscriptions in SubscriptionStore
    def disconnect(self, code):
        pass
