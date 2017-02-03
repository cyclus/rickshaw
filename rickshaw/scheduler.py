"""Scheduler abstract class that represents how to query for currently running jobs,
ask request more jobs to be run, and ask for a Cyclus server as needed.
"""
from abc import ABCMeta, abstractmethod


class Scheduler(metaclass=ABCMeta):
    """A metaclass for all schedulers."""

    @abstractmethod
    def start_cyclus_server(self):
        """Starts up a cyclus server at a remote location."""
        ...

    @abstractmethod
    def shutdown_cyclus_server(self):
        """Starts up a cyclus server at a remote location."""
        ...

    @abstractmethod
    def queue(self):
        """Obtains the current queue status and retuns the jobs that are scheduled
        and status of each job.
        """
        ...

    @abstractmethod
    def schedule(self, sim):
        """Schedules a simulation to be executed."""
        ...
