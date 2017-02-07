"""Scheduler for running via docker."""
import time

import docker

from rickshaw.scheduler import Scheduler


class DockerScheduler(Scheduler):
    """A base docker scheduler"""

    def __init__(self):
        self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        self.cyclus_container = None
        self.cyclus_tag = "ergs/cyclus-server-dev"
        self.cyclus_cmd = "--debug"
        self.cyclus_server_ready = False
        self.gathered_annotations = False

    def __del__(self):
        self.stop_cyclus_server()

    def start_cyclus_server(self):
        """Starts up a cyclus server at a remote location."""
        print("starting cyclus server")
        cc = self.cyclus_container = self.client.containers.run(self.cyclus_tag,
                                                                self.cyclus_cmd,
                                                                ports={'4242/tcp': 4242},
                                                                detach=True)
        print("cyclus server started")
        time.sleep(3)
        self.cyclus_server_ready = True
        for line in cc.logs(stream=True):
            print('[cyclus] ' + line.decode(), end='')

    def stop_cyclus_server(self):
        """Stops the cyclus server running in a remote location"""
        if self.cyclus_container is not None:
            self.cyclus_container.stop()
            self.cyclus_container = None
        self.cyclus_server_ready = False

    def queue(self):
        """Obtains the current queue status and retuns the jobs that are scheduled
        and status of each job.
        """
        ...

    def schedule(self, sim):
        """Schedules a simulation to be executed."""
        ...
