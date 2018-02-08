import json
from enum import Enum

import asyncio
from asgiref.sync import AsyncToSync, async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from channels.layers import get_channel_layer


# See https://github.com/apollographql/subscriptions-transport-ws/blob/master/PROTOCOL.md
class GQLMessageType(Enum):
    GQL_CONNECTION_ACK = 'connection_ack'  # Server -> Client
    GQL_CONNECTION_ERROR = 'connection_error'  # Server -> Client
    GQL_START = 'start'  # Client -> Server
    GQL_DATA = 'data'  # Server -> Client
    GQL_ERROR = 'error'  # Server -> Client
    GQL_COMPLETE = 'complete'  # Server -> Client
    GQL_STOP = 'stop'  # Client -> Server

    @classmethod
    def contains(self, val):
        return val in [item.value for item in GQLMessageType]


# Placeholder
class SubscriptionType(Enum):
    AUTO_CLOSED_DISCUSSION = 'autoClosedDiscussion'
    STALE_DISCUSSION = 'staleDiscussion'

    @classmethod
    def contains(self, val):
        return val in [item.value for item in SubscriptionType]


def build_message(type, payload=None, errors=None):
    """Build GraphQL-compliant message"""
    assert isinstance(type, GQLMessageType), 'Type must be of type GQLMessageType'

    message = {'type': type.value}

    if payload:
        message.update({'payload': payload})

    if errors:
        errors_payload = {'errors': [{'message': error_message} for error_message in errors]}
        if payload:
            message['payload'].update(errors_payload)
        else:
            message['payload'] = errors_payload

    return message


tasks = set()


async def stop(self):
    print('ayy')
    if tasks:
        await asyncio.wait(tasks)


def send_subscription_message_to_group(group_name, payload):
    """Send a message to group"""
    assert isinstance(payload, dict), 'Payload must be an object'
    channel_layer = get_channel_layer()
    message = build_message(GQLMessageType.GQL_DATA, payload)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    print({'text': json.dumps(message), 'type': 'receive_group_json'})
    future = asyncio.ensure_future(
        channel_layer.group_send(group_name, {'text': json.dumps(message),
                                              'type': 'receive_group_json'}),
    )
    yield from future.__await__()


class SubscriptionConsumer(JsonWebsocketConsumer):
    # TODO: Authenticate and potentially reject
    def connect(self):
        try:
            self.accept()
            self.send_message(GQLMessageType.GQL_CONNECTION_ACK)
        except Exception as e:
            self.send_message(GQLMessageType.GQL_ERROR, errors=[str(e)])

    def add_to_group(self, group_name):
        AsyncToSync(self.channel_layer.group_add)(group_name, self.channel_name)

    def remove_from_group(self, group_name):
        AsyncToSync(self.channel_layer.group_discard)(group_name, self.channel_name)

    def send_message(self, type, payload=None, errors=None):
        msg = build_message(type, payload, errors)
        self.send_json(msg)

    def receive_group_json(self, message):
        """Receive group messages and send to client"""
        self.send_json(json.loads(message.get('text')))

    # TODO: Add subscription type to schema
    # TODO: Validate query with graphql and schema
    # TODO: Delay execution (?) something about depromise
    # TODO: What about subscriptions with variables?
    # TODO: Store subscription in SubscriptionStore
    # TODO: Include self.channel_name in SubscriptionStore
    # TODO: Apollo uses codes to subscribe / unsubscribe
    # TODO: Option to use subscribe vs. subscription
    def receive_json(self, message, **kwargs):
        if message.get('type') == GQLMessageType.GQL_START.value:
            if SubscriptionType.contains(message['payload']['query']):
                self.add_to_group(message['payload']['query'])
            else:
                print(message['payload']['query'])
                self.send_message(type=GQLMessageType.GQL_ERROR, errors=['Unknown subscription'])
        elif message.get('type') == GQLMessageType.GQL_STOP.value:
            if SubscriptionType.contains(message['payload']['query']):
                self.remove_from_group(message['payload']['query'])
            else:
                self.send_message(type=GQLMessageType.GQL_ERROR, errors=['Unknown subscription'])
        else:
            self.send_message(type=GQLMessageType.GQL_ERROR, errors=['Unknown message type'])

    # TODO: Remove subscriptions in SubscriptionStore for this self.channel_name
    def disconnect(self, code):
        pass
