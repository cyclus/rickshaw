"""Scheduler for running via docker."""
import time

import docker

from rickshaw.scheduler import Scheduler


class DockerScheduler(Scheduler):
    """A base docker scheduler"""

    def __init__(self, debug=False, **kwargs):
        #self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        self.client = docker.from_env()
        self.cyclus_container = None
        self.server_tag = "ergs/cyclus-server-dev"
        if debug:
            self.server_cmd = "--debug"
        else:
            self.server_cmd = ""
        self.cyclus_server_ready = False
        self.gathered_annotations = False
        self.ncpu = self.client.info()['NCPU']

    def __del__(self):
        self.stop_cyclus_server()

    def start_cyclus_server(self):
        """Starts up a cyclus server at a remote location."""
        print("starting cyclus server")
        cc = self.cyclus_container = self.client.containers.run(self.server_tag,
                                                                self.server_cmd,
                                        ports={'4242/tcp': ('127.0.0.1', 4242)},
                                                          hostname='127.0.0.1:',
        #                                       links=[("rickshaw", "rickshaw")],
                                                        name="cyclus_server",
                                                        publish_all_ports=True,
                                                                detach=True)
        print(self.client.networks.get('bridge').attrs['Containers'][cc.id]['IPv4Address'])
        while not cc.attrs['NetworkSettings']['Networks']['bridge']['IPAddress']:
            print(cc.attrs['NetworkSettings'])
            print("waiting on IP.")
            time.sleep(1)
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
        return [(c.id, c.status) for c in self.client.containers.list()]

    def schedule(self, sim):
        """Schedules a simulation to be executed."""
        print("would have scheduled sim: ", repr(sim))

    def want_n_more_jobs(self):
        """Determine how many more new jobs to schedule."""
        n = self.ncpu + 1 - len(self.queue())
        return n
