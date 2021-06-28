from slack_sdk import WebClient
import utilix
import os
import logging


class DaqSlackUpload:
    """DAQ wrapper for uploading files and sending messages to the slack-bot"""

    def __init__(self, channel_name, token=None, channel_key=None):
        if token is None:
            token = utilix.uconfig.get('slack', 'slack_api_token')
        if channel_key is None:
            channel_key = utilix.uconfig.get('slack', channel_name)
        self.channel_key = channel_key
        self.client = WebClient(token=token)
        self.log = logging.getLogger('Slackbot')
        self.log.debug(f'Writing to {channel_name}:{self.channel_key}')

    def send_message(self, message, channel_key=None, **kwargs):
        if channel_key is None:
            channel_key = self.channel_key
        response = self.client.chat_postMessage(channel=channel_key,
                                                text=message,
                                                **kwargs,
                                                )
        self.log.debug(f'Got {response} while writing {message} to {channel_key}')
        return response

    def send_message_threaded(self, message, max_messages=35, **kwargs):
        """
        Send a message and immediately reply in a tread to the message. This is
        especially useful for messages that are stack-able. For instance, a
        warning and a full description of the warning that is then send in a
        thread.

        :param message: List or tuple of messages. The first message is posted,
            the following messages are posted in a thread as a reply to the
            main (first) message
        :param max_messages: the max number of messages one can send.
        :param kwargs: are passed of to the self.send_message
        :return: response
        """
        if not isinstance(message, (tuple, list)):
            ValueError("Threaded messages must be a list of messages")
        if not (1 < len(message) <= max_messages):
            raise ValueError(f'Got {len(message)} messages')
        message_iter = iter(message)
        first_response = self.send_message(next(message_iter), **kwargs)
        time_stamp = first_response.data['ts']

        for mes in message_iter:
            last_response = self.send_message(mes,
                                              thread_ts=time_stamp,
                                              **kwargs)
        return last_response

    def send_file(self, message, file_name, channel_key=None):
        if channel_key is None:
            channel_key = self.channel_key
        if not os.path.exists(file_name):
            raise FileNotFoundError(f'{file_name} does not exits')
        response = self.client.files_upload(channels=channel_key,
                                            file=file_name,
                                            title=message)
        self.log.debug(f'Got {response} while writing {message} and {file_name} to {channel_key}')
        return response
