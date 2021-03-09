import daq_bot
from slack import WebClient
from slack.errors import SlackApiError
import utilix
import os
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M')
log = logging.getLogger()


class DaqSlackUpload:
    """DAQ wrapper for uploading files and sending messages to the """
    def __init__(self, channel_name):
        token = utilix.uconfig.get('slack', 'slack_api_token')
        self.client = WebClient(token=token)
        self.channel_key = utilix.uconfig.get('slack', channel_name)
        log.debug(f'Writing to {channel_name}:{self.channel_key}')

    def send_message(self, message):
        response = self.client.chat_postMessage(self.channel_key, message)
        log.debug(f'Got {response} while writing {message} to {self.channel_key}')
        return response

    def send_file(self, message, file_name):
        if not os.path.exists(file_name):
            raise FileNotFoundError(f'{file_name} does not exits')
        response = self.client.files_upload(channels=self.channel_key,
                                            file=file_name,
                                            title=message)
        log.debug(f'Got {response} while writing {message} and {file_name} to {self.channel_key}')
        return response
