from threading import Thread

class Job(Thread):

    """libnixcore job """
    
    def __init__(self):
        super(Job,self).__init__()