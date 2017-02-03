"""Scheduler for running via docker."""
import docker

from rickshaw.scheduler import Scheduler


class DockerScheduler(Scheduler):
    """A base docker scheduler"""

    def start_cyclus_server(self):
        """Starts up a cyclus server at a remote location."""
        ...

    def shutdown_cyclus_server(self):
        """Starts up a cyclus server at a remote location."""
        ...

    def queue(self):
        """Obtains the current queue status and retuns the jobs that are scheduled
        and status of each job.
        """
        ...

    def schedule(self, sim):
        """Schedules a simulation to be executed."""
        ...
