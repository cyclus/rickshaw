"""The asynchronous rickshaw server that communicates with scheduling queues and
provides randomly generated input files.
"""
import sys
import json
import socket
import asyncio
import concurrent.futures
from argparse import ArgumentParser

import docker
import websockets

from rickshaw import choose_archetypes
from rickshaw.docker_scheduler import DockerScheduler
from rickshaw.generate import generate


SCHEDULER = None
SEND_QUEUE = asyncio.Queue()

def all_archetypes():
    arches = choose_archetypes.DEFAULT_SOURCES | choose_archetypes.DEFAULT_SINKS
    for v in choose_archetypes.NICHE_ARCHETYPES.values():
        arches |= v
    return arches


async def gather_annotations(frequency=0.001):
    """The basic consumer of actions."""
    all_arches = all_archetypes()
    curr_arches = set(choose_archetypes.ANNOTATIONS.keys())
    staged_tasks = []
    while curr_arches < all_arches:
        if SEND_QUEUE.qsize() > 0:
            await asyncio.sleep(frequency)
            curr_arches = set(choose_archetypes.ANNOTATIONS.keys())
            continue
        for arche in all_arches - curr_arches:
            msg = {'event': 'agent_annotations', 'params': {'spec': arche}}
            msg = json.dumps(msg)
            print(msg)
            action_task = asyncio.ensure_future(SEND_QUEUE.put(msg))
            staged_tasks.append(action_task)
        if len(staged_tasks) > 0:
            await asyncio.wait(staged_tasks)
            staged_tasks.clear()
        await asyncio.sleep(frequency)
        curr_arches = set(choose_archetypes.ANNOTATIONS.keys())


async def get_send_data():
    """Asynchronously grabs the next data to send from the queue."""
    data = await SEND_QUEUE.get()
    return data


async def queue_message_action(message):
    event = json.loads(message)
    params = event.get("params", {})
    kind = event["event"]
    if kind == 'agent_annotations':
        spec = params['spec']
        choose_archetypes.ANNOTATIONS[spec] = event['data']
    else:
        print("ignoring recived " + kind + " event")


async def websocket_handler(websocket, path):
    """Sends and recieves data via a websocket."""
    while True:
        recv_task = asyncio.ensure_future(websocket.recv())
        send_task = asyncio.ensure_future(get_send_data())
        done, pending = await asyncio.wait([recv_task, send_task],
                                           return_when=asyncio.FIRST_COMPLETED)
        # handle incoming
        if recv_task in done:
            message = recv_task.result()
            print("got message", message)
            await queue_message_action(message)
        else:
            recv_task.cancel()
        # handle sending of data
        if send_task in done:
            message = send_task.result()
            await websocket.send(message)
        else:
            send_task.cancel()


async def websocket_client(host, port, scheduler, frequency=0.001):
    """Runs a websocket client on a host/port."""
    #while not scheduler.cyclus_server_ready:
    #    await asyncio.sleep(frequency)
    url = 'ws://{}:{}'.format(host, port)
    #connected = False
    #while not connected:
    #    try:
    #        async with websockets.connect(url) as websocket:
    #            connected = True
    #            await websocket_handler(websocket, None)
            #connection = websockets.connect(url)
            #connected = True
    #    except websockets.exceptions.InvalidHandshake:
    #        pass
    #async with websockets.connect(url) as websocket:
    async with websockets.connect(url) as websocket:
        await websocket_handler(websocket, None)


async def start_cyclus_server(loop, executor):
    """Starts up remote cyclus server"""
    run_task = loop.run_in_executor(executor, SCHEDULER.start_cyclus_server)
    await asyncio.wait([run_task])


def _start_debug(loop):
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('websockets.server')
    logger.setLevel(logging.ERROR)
    logger.addHandler(logging.StreamHandler())
    loop.set_debug(True)


def _find_open_port(host, port):
    found = False
    while not found:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((host, port))
        except socket.error as e:
            if e.errno == 98:
                port += 1
                continue
            else:
                raise
        finally:
            s.close()
        found = True
    return port


def make_parser():
    """Makes the argument parser for the rickshaw server."""
    p = ArgumentParser("rickshaw-server", description="Rickshaw Server CLI")
    p.add_argument('--debug', action='store_true', default=False,
                   dest='debug', help="runs the server in debug mode.")
    p.add_argument('--host', dest='host', default='localhost',
                   help='hostname to run the server on')
    p.add_argument('-p', '--port', dest='port', type=int, default=4242,
                   help='port to run the server on')
    p.add_argument('-n', '--nthreads', type=int, dest='nthreads', default=4,
                   help='Maximum number of thread workers to run with.')
    return p


def main(args=None):
    global SCHEDULER
    p = make_parser()
    ns = p.parse_args(args=args)
    # start up tasks
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=ns.nthreads)
    loop = asyncio.get_event_loop()
    SCHEDULER = scheduler = DockerScheduler()
    if ns.debug:
        _start_debug(loop)
    #open_port = _find_open_port(ns.host, ns.port)
    #if open_port != ns.port:
    #    msg = "port {} already bound, next available port is {}"
    #    print(msg.format(ns.port, open_port), file=sys.stderr)
    #    ns.port = open_port
    #server = websockets.serve(websocket_handler, ns.host, ns.port)
    #server = websockets.connect(websocket_handler, ns.host, ns.port)
    print("serving rickshaw at http://{}:{}".format(ns.host, ns.port))
    # run the loop!
    try:
        loop.run_until_complete(asyncio.gather(
            #asyncio.ensure_future(server),
            asyncio.ensure_future(websocket_client(ns.host, ns.port, scheduler)),
            asyncio.ensure_future(gather_annotations()),
            #asyncio.ensure_future(start_cyclus_server(loop, executor)),
            ))
    finally:
        if not loop.is_closed():
            loop.close()


if __name__ == '__main__':
    main()
