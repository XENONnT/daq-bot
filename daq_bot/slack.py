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

    def send_message(self, message, channel_key=None):
        if channel_key is None:
            channel_key = self.channel_key
        response = self.client.chat_postMessage(channel=channel_key,
                                                text=message)
        self.log.debug(f'Got {response} while writing {message} to {channel_key}')
        return response

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
