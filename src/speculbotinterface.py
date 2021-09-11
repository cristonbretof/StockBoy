from abc import abstractmethod

class SpeculBotInterface:

    def __init__(self):
        pass

    @abstractmethod
    def wait_for_data(self):
        raise NotImplementedError('Waiting For Data')

    @abstractmethod
    def send_results(self, results):
        raise NotImplementedError('Send Results: {}'.format(results))