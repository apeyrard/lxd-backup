import logging

from pylxd import Client
from pylxd.exceptions import LXDAPIException

logger = logging.getLogger(__name__)


class Container():
    def __init__(self, name):
        self._name = name
        self.__container = Client().containers.get(name)

    def start(self):
        try:
            self.__container.start(wait=True)
        except LXDAPIException as e:
            if e.response.json()['metadata']['err'] == 'The container is already running':
                pass

    def stop(self):
        try:
            self.__container.stop(wait=True)
        except LXDAPIException as e:
            if e.response.json()['metadata']['err'] == 'The container is already stopped':
                pass

    def is_running(self):
        return self.__container.status == 'Running'

    def publish(self):
        logger.info(f'publishing container: {self._name}')
        restart = self.is_running()
        self.stop()
        image = self.__container.publish(wait=True)
        if restart:
            self.start()
        return image
