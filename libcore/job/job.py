from threading import Thread

class Job(Thread):

    def __init__(self):
        super(Job,self).__init__()