from .job import Job


class Isolated(Job):

    """Libnixcore Application Isolated Task which has no connection but to Job and Thread"""

    def __init__(self):
        super(Isolated, self).__init__()
