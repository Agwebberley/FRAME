from aws_utils import listener
from frame.models import LogMessage


@listener("*")
def log_message_listener(channel, action, data):
    """
    Listener function to log messages to the LogMessage model.

    This function listens to all channels and logs the received messages,
    including the channel name, action performed, and data associated with the event.

    :param channel: The name of the channel where the event occurred.
    :type channel: str
    :param action: The action performed on the channel (e.g., 'created', 'updated', 'deleted').
    :type action: str
    :param data: The data associated with the event.
    :type data: dict
    """
    LogMessage.objects.create(channel=channel, action=action, data=data)
    print(f"Logged message: {channel} - {action} - {data}")
