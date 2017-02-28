"""Scheduler abstract class that represents how to query for currently running jobs,
ask request more jobs to be run, and ask for a Cyclus server as needed.
"""
from abc import ABCMeta, abstractmethod


class Scheduler(metaclass=ABCMeta):
    """A metaclass for all schedulers."""

    ncpu = None
    cyclus_server_host = None
    cyclus_server_ready = False
    gathered_annotations = False

    @abstractmethod
    def start_cyclus_server(self):
        """Starts up a cyclus server at a remote location."""
        ...

    @abstractmethod
    def stop_cyclus_server(self):
        """Stops up a cyclus server at a remote location."""
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

    @abstractmethod
    def want_n_more_jobs(self):
        """How many more jobs should be scheduled."""
        ...
