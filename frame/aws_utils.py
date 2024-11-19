import boto3
from django.conf import settings

sns_client = boto3.client("sns", region_name=settings.AWS_REGION)
sqs_client = boto3.client("sqs", region_name=settings.AWS_REGION)


def get_or_create_topic(channel):
    """
    Get or create an SNS topic for the given channel.

    :param channel: The name of the channel (SNS topic).
    :type channel: str
    :return: The ARN of the SNS topic, or None if there was an error.
    :rtype: str or None
    """
    try:
        response = sns_client.create_topic(Name=channel)
        return response["TopicArn"]
    except Exception as e:
        print(f"Error creating/getting SNS topic {channel}: {e}")
        return None


def publish_event(channel, message):
    """
    Publish an event message to the SNS topic for the given channel.

    :param channel: The name of the channel (SNS topic).
    :type channel: str
    :param message: The message to publish.
    :type message: str
    """
    try:
        topic_arn = get_or_create_topic(channel)
        if topic_arn:
            sns_client.publish(TopicArn=topic_arn, Message=message)
    except Exception as e:
        print(f"Error publishing event to {channel}: {e}")


listeners = {}


def listener(channel):
    """
    Decorator to register a listener function for a given channel.

    :param channel: The name of the channel to listen to.
    :type channel: str
    :return: The decorator function.
    :rtype: function
    """

    def decorator(func):
        if channel not in listeners:
            listeners[channel] = []
        listeners[channel].append(func)
        return func

    return decorator


def get_listeners(channel):
    """
    Get the list of listener functions registered for the given channel.

    :param channel: The name of the channel.
    :type channel: str
    :return: List of listener functions.
    :rtype: list
    """
    return listeners.get(channel, [])


def get_channels():
    """
    Get the list of channels that have registered listeners.

    :return: List of channel names.
    :rtype: list
    """
    return listeners.keys()
