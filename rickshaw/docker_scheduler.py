"""Scheduler for running via docker."""
import time

import docker
try:
    from pprintpp import pprint
except ImportError:
    from pprint import pprint

from rickshaw.scheduler import Scheduler


class DockerScheduler(Scheduler):
    """A base docker scheduler"""

    def __init__(self, debug=False, **kwargs):
        self.client = docker.from_env() 
        try:
            try_test = self.client.nodes.list()
        except:
            print( '***************************************************\n'+
                   'This container probably failed to connect to docker. '+
                   'Remember to give this container/service access to the '+
                   'docker socket on the host machine with the following command: '+
                   '-v /var/run/docker.sock:/var/run/docker.sock\n' +
                   '***************************************************')       
        self.cyclus_container = None
        self.server_tag = "ergs/cyclus-server-dev"
        if debug:
            self.server_cmd = "--debug"
        else:
            self.server_cmd = ""
        self.cyclus_server_name = "rickshaw_metadata_server"
        self.cyclus_server_host = None
        self.cyclus_server_ready = False
        self.gathered_annotations = False
        self._have_swarm = False
        self._find_ncpu()

    def _find_ncpu(self):        
        try:
            # get NCPUs for swarm
            ncpu = 0.0
            for node in self.client.nodes.list():
                ncpu += node.attrs['Description']['Resources']['NanoCPUs'] * 1e-9
            self._have_swarm = True
        except docker.errors.APIError:
            print('except')
            # get NCPUs for local host
            ncpu = self.client.info()['NCPU']
            self._have_swarm = False
        self.ncpu = int(ncpu)

    def __del__(self):
        self.stop_cyclus_server()

    def start_cyclus_server(self):
        """Starts up a cyclus server at a remote location."""
        print("starting cyclus server")
        cc = self.cyclus_container = self.client.containers.run(self.server_tag,
                                                                self.server_cmd,
                                        ports={'4242/tcp': ('127.0.0.1', 4242)},
                                                   name=self.cyclus_server_name,
                                                         publish_all_ports=True,
                                                                    detach=True)
        host = self.client.networks.get('bridge').attrs['Containers'][cc.id]['IPv4Address']
        if '/' in host:
            self.cyclus_server_host, _, _ = host.rpartition('/')
        else:
            self.cyclus_server_host = host
        print("cyclus server started at host " + host)
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
        #print("would have scheduled sim: ", repr(sim))

    def want_n_more_jobs(self):
        """Determine how many more new jobs to schedule."""
        n = self.ncpu*2 - len(self.queue())
        print("will want, " + str(n))
        pprint(self.client.swarm.attrs)
        return n
