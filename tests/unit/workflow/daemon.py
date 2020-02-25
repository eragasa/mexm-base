import os
from crontab import Crontab

def get_user_name_from_environ(self):
    """ get username from the environment variables

    Returns:
        str: username
    """
    uname = os.environ['USER']
    return uname


class MexmWorkflowDaemon():
    def __init__(self, name):
        self.name = name

    def start(self):

        print('[{}]'.format(self.name))

    def poll(self):
        print('[{}]'.format(self.name))

    def end(self):
        print('[{}]'.format(self.name))


class MexmWorkflowScheduler(MexmWorkflowDaemon):

    def start(self):
        print('[{}]'.format(self.name))

    def poll(self):
        print('[{}]'.format(self.name))

    def end(self):
        print('[{}]'.format(self.name))

class MexmWorkflowProducer(MexmWorkflowDaemon):

    def start(self):
        print('[{}]'.format(self.name))

    def poll(self):
        print('[{}]'.format(self.name))

    def end(self):
        print('[{}]'.format(self.name))

class MexmWorkflowConsumer(MexmWorkflowDaemon):

    def start(self):
        print('[{}]'.format(self.name))

    def poll(self):
        print('[{}]'.format(self.name))

    def end(self):
        print('[{}]'.format(self.name))

class MexmWorkflowConsumerProducer(MexmWorkflowDaemon):
    def __init__(self):
        super().__init__(self)

    def start(self):
        print('[{}]'.format(self.name))

    def poll(self):
        print('[{}]'.format(self.name))

    def end(self):
        print('[{}]'.format(self.name))

class MexmWorkflowFactory():
    factories = {
        'producer':MexmWorkflowScheduler,
        'consumer':MexmWorkflowConsumer,
        'consumer_producer':MexmWorkflowConsumerProducer,
    }