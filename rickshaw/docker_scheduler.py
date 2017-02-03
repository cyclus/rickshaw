"""Scheduler for running via docker."""
import docker

from rickshaw.scheduler import Scheduler


class DockerScheduler(Scheduler):
    """A base docker scheduler"""

    def __init__(self):
        self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')

    def start_cyclus_server(self):
        """Starts up a cyclus server at a remote location."""
        self.client.containers.run("ubuntu", "echo hello world")

    def queue(self):
        """Obtains the current queue status and retuns the jobs that are scheduled
        and status of each job.
        """
        ...

    def schedule(self, sim):
        """Schedules a simulation to be executed."""
        ...
