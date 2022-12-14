import os
import signal
import time
import json
from libcore.job import Job


class Maintainer:

    """libnixcore Application maintainer """

    def __init__(self):
        self.running = True
        signal.signal(signal.SIGINT, self._handler)
        signal.signal(signal.SIGTERM, self._handler)
        self.tasks = []
        self.settings = None
        env = 'CORE_SETTINGS_PATH'
        if env in os.environ:
            try:
                with open(os.environ[env]) as f:
                    self.settings = json.load(f)
            except FileNotFoundError:
                pass

    def _handler(self, sig, frame):
        self.running = False

    def get_settings(self, default_settings):
        """
        Get given libnixcore settings.

        Args:
            default_settings (dict): default settings

        Returns:
            dict: updated settings

        Notes:
            Copy default_settings and overwrite it by given libnixcore settings.
        """

        if not isinstance(default_settings, dict):
            raise TypeError("default_settings must be dict.")
        settings = default_settings.copy()
        if self.settings is not None:
            settings.update(self.settings)
        return settings

    def subscribe(self, task):
        """
        Subscribe to the maintainer

        Args:
            task (:class:`~libcore.job.job.Job`): job
        """

        if not issubclass(type(task), Job):
            raise TypeError("type(task) must be a subclass of libcore.job.Job")
        self.tasks.append(task)

    def run(self):
        """Start application"""
        for task in self.tasks:
            task.start()

        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        except BaseException:
            raise

        for task in self.tasks:
            task.stop()
        for task in self.tasks:
            task.join()
