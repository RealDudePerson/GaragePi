import logging
import requests
import json

class SignalNotification:
    signal_service = ''
    signal_group_id = ''
    signal_number = ''

    def __init__(self,signal_service: str, signal_group_id: str, signal_number, event_name: str, logger: logging.Logger):
        """
        :param signal_service: The ip/hostname that signal-cli is running on 
        :param signal_group_id: The signal group id for the notification delivery
        :param signal_number: The sender account number for the sinal account
        :param event_name: The name of the event to trigger
        :param logger: Logger for logging purposes
        """
        if logger is None:
            raise Exception("Logger is missing!")
        if not signal_service:
            logger.debug('Signal: Signal Service provided!')
            raise Exception("NO Signal Service provided!")
        if not signal_group_id:
            logger.debug('Signal: NO signal_group_id provided!')
            raise Exception("NO signal_group_id provided!")
        if not signal_number:
            logger.debug('Signal: NO signal_number provided!')
            raise Exception("NO signal_number provided!")
        if not event_name:
            logger.debug('Signal: NO event name provided')
            raise Exception("NO event name provided!")
        logger.info('Created SignalNotification object %s' %(event_name))
        self.signal_service = signal_service
        self.signal_group_id = signal_group_id
        self.signal_number = signal_number
        self.event_name = event_name
        self.logger = logger
    
    def trigger(self):
        self.logger.info("Works.")
        self.logger.debug(self.signal_service)
        payload = {
            "message": self.event_name,
            "number": self.signal_number,
            "recipients": [self.signal_group_id],
            "text_mode": "normal",
            "notify_self": False
        }
        url = "http://" + self.signal_service + "/v2/send"
        self.logger.info('Trying to hit the signal cli service %s' %(url))
        try:
            response = requests.post(
                url,
                headers={
                    "accept": "application/json",
                    "Content-Type": "application/json"
                },
                data=json.dumps(payload)
            )
            response.raise_for_status()
        except requests.RequestException as e:
            self.logger.info('Signal notification failed')
            self.logger.info(e)
