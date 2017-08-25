"""This provides support for Rickshaw in Blue Waters. It generates the 
input files for a cyclus and then calls the script to run the input files.
"""

import os
import sys
import time
import json
import socket
import asyncio
import concurrent.futures
from argparse import ArgumentParser
from textwrap import dedent
from subprocess import call

import docker
import websockets

from rickshaw.docker_scheduler import DockerScheduler
from rickshaw.server_scheduler import ServerScheduler
import rickshaw.generate as generate

CYCLUS_SCRIPT = \
    """
    #!/bin/bash
    cyclus %(in_dir)s/$ALPS_APP_PE.json -o \
            %(out_dir)s/$ALPS_APP_PE.%(out_type)s \
            > %(log_dir)s/out_$ALPS_APP_PE.log
    """

PBS_SCRIPT = \
    """
    #!/bin/bash
    #PBS -l gres=shifter
    #PBS -v UDI=arfc/cyclus_blue_waters:latest
    #PBS -l nodes=%(nodes)s:ppn=%(ppn)s:xe
    #PBS -l walltime=%(walltime)s
    export CRAY_ROOTFS=UDI
    export LD_LIBRARY_PATH="/usr/lib/lapack:/usr/lib/libblas:$LD_LIBRARY_PATH"
    export PYTHONPATH="/cyclus/build:$PYTHONPATH"
    cd $PBS_O_WORKDIR
    aprun -n 1 -N 1 -d 1 -b -- /usr/local/bin/rickshaw -i %(spec_file)s -n %(n)s
    mv *.json %(in_dir)s
    start_time=`date +%%s`
    aprun -n %(n)s -N %(N)s -d 1 -b -- cyclus_script.sh
    end_time=`date +%%s`
    echo Execution time: `expr $end_time - $start_time` s > time.txt
    """

def render_cyclus_script(out_type="sqlite", in_dir=".", out_dir=".",
        log_dir="."):
    """
    Renders the cyclus execution script
    Parameters
    ----------
    out_type : str
        Output type ('sqlite' or 'h5')
    in_dir : str
        Inputs directory
    out_dir : str
        Outputs directory
    log_dir : str
        Logs directory
    Returns
    -------
    str
        Rendered cyclus execution script
    """

    rendered_cyclus_script = dedent(CYCLUS_SCRIPT) % {
            "in_dir" : in_dir, "out_dir" : out_dir, "out_type" : out_type,
            "log_dir" : log_dir}

    return rendered_cyclus_script.strip()

def render_pbs_script(nodes, ppn, walltime, spec_file, in_dir):
    """
    Renders the PBS script
    Parameters
    ----------
    nodes : int
        Number of nodes
    ppn : int
        Number of processors per node
    walltime : str
        Wall time
    spec_file : str
        Specification file
    in_dir : str
        Inputs directory
    Returns
    -------
    str
        Rendered PBS script
    """

    rendered_pbs_script = dedent(PBS_SCRIPT) % {"nodes" : str(nodes),
            "ppn" : str(ppn), "walltime" : walltime, "n" : str(nodes*ppn),
            "N" : str(ppn), "spec_file" : spec_file, "in_dir" : in_dir}

    return rendered_pbs_script.strip()

def write_to_files(cyclus_script, pbs_script):
    """
    Writes PBS script and execution script to corresponding files
    Parameters
    ----------
    cyclus_script : str
        Cyclus execution script
    pbs_script : str
        PBS script
    """
    with open("cyclus_script.sh", "w+") as f:
        f.write(cyclus_script)
    call("chmod +x cyclus_script.sh", shell=True)

    with open("pbs_script.pbs", "w+") as f:
        f.write(pbs_script)

def generate_scripts(nodes, ppn):
    """
    Calls the functions to build the cyclus and pbs scripts
    
    Parameters
    ----------
    nodes : int
        number of nodes to deploy the cyclus jobs on
    ppn : int
        processors per node
    """
    args = parser.parse_args()

    cyclus_script = render_cyclus_script(out_type='h5',
            in_dir='.', out_dir='.', log_dir='.')

    pbs_script = render_pbs_script(nodes, ppn, '00:05:00',
            '', '.')

    write_to_files(cyclus_script, pbs_script)
