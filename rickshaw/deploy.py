"""Functions used for the facility deployment schemes for rickshaw
"""

import json
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np

def read_file(inputfile):
    dict = inputfile
    inst = dict['simulation']['region']['institution']['config']['DeployInst']
    sim_length = dict['simulation']['control']['duration']
    rpx, r1px = 0, 0
    for obj in dict['simulation']['facility']:
        if obj['name'] == 'Reactor':
            rpx = obj['config']['Reactor']['power_cap']
        if obj['name'] == 'Reactor1':
            r1px = obj['config']['Reactor']['power_cap']
    builds = inst['n_build']['val']
    protos = inst['prototypes']['val']
    times = inst['build_times']['val']
    lifes = inst['lifetimes']['val']
    prototypes = {}
    for proto in protos:
        prototypes[proto] = {}
        prototypes[proto]['times'] = []
        prototypes[proto]['builds'] = []
        prototypes[proto]['fulltime'] = {}
        prototypes[proto]['fullpower'] = {}
        prototypes[proto]['sumtime'] =[]
        prototypes[proto]['deploy'] = []
        prototypes[proto]['power'] = []
        if proto == 'Reactor': prototypes[proto]['px'] = rpx
        elif proto == 'Reactor1': prototypes[proto]['px'] = r1px
        else: prototypes[proto]['px'] = 0
    for i in range(len(protos)):
        prototypes[protos[i]]['times'].append(times[i])
        prototypes[protos[i]]['builds'].append(builds[i])
        if times[i] in prototypes[protos[i]]['fulltime']:
            prototypes[protos[i]]['fulltime'][times[i]] += builds[i]
            prototypes[protos[i]]['fullpower'][times[i]] += builds[i] * prototypes[protos[i]]['px']      
        else:
            prototypes[protos[i]]['fulltime'][times[i]] = builds[i]
            prototypes[protos[i]]['fullpower'][times[i]] = builds[i] * prototypes[protos[i]]['px']     
        prototypes[protos[i]]['fulltime'][times[i]+(lifes[i]*12)] = builds[i]*-1
        prototypes[protos[i]]['fullpower'][times[i]+(lifes[i]*12)] = builds[i]*-1*prototypes[protos[i]]['px'] 
    for proto in prototypes.keys():
        p = prototypes[proto]
        for date in p['fulltime'].keys():
            p['sumtime'].append(date)
        p['sumtime'].sort()
        i = 1
        p['deploy'].append(p['fulltime'][p['sumtime'][0]])
        while i < len(p['sumtime']):
            p['deploy'].append(p['fulltime'][p['sumtime'][i]] + p['deploy'][i-1])
            i+=1
        if proto == 'Reactor':
            for n in p['deploy']:
                p['power'].append(n*rpx)
        if proto == 'Reactor1':
            for n in p['deploy']:
                p['power'].append(n*r1px)
    for proto in protos:
        prototypes[proto]['deploy'] = np.asarray(prototypes[proto]['deploy'])
        prototypes[proto]['power'] = np.asarray(prototypes[proto]['power'])
    return prototypes, sim_length

def plot_fac_numbers(prototypes, facs):
    for facs in facs:
        plt.plot(prototypes[fac]['sumtime'], prototypes[fac]['deploy'], label=fac)
    plt.xlabel("Months")
    plt.ylabel("Number of facilities")
    plt.legend()
    plt.show()

def plot_fac_powers(prototypes, facs):
    for facs in facs:
        plt.plot(prototypes[fac]['sumtime'], prototypes[fac]['power'], label=fac)
    plt.legend()
    plt.xlabel("Months")
    plt.ylabel("Power (MWe)")
    plt.show()

def combine_power(prototypes, sim_length):
    totalp = []
    power = {}
    for fac in prototypes:
        for k,v in prototypes[fac]['fullpower'].items():
            if k < sim_length:
                if k in power:
                    power[k] += v
                else:
                    power[k] = v
    sumt = list(power.keys())
    sumt.sort()
    for date in sumt:
        totalp.append(power[date])
    totalp = np.asarray(totalp)
    totalp = np.cumsum(totalp)
    return sumt, totalp

def plot_total_power(inputfile, parameters):
    facs, pstart, rate = parameters['facs'], parameters['pstart'], parameters['rate']
    prototypes, sim_length = read_file(inputfile)
    sumt, totalp = combine_power(prototypes, sim_length)
    pgrow = demand_curve(pstart, rate, sumt)
    plt.figure(1)
    plt.plot(sumt, totalp, 'r', label="Total Power")
    plt.plot(sumt, pgrow, 'b', label="Expected")
    plt.figure(2)
    plt.semilogy(sumt, totalp, 'r', label="Total Power")
    plt.semilogy(sumt, pgrow, 'b', label="Expected")
    plt.xlabel("Months")
    plt.ylabel("Power (MWe)")
    plt.figure(3)
    for fac in facs:
        plt.plot(prototypes[fac]['sumtime'], prototypes[fac]['deploy'], label=fac)
    plt.xlabel("Months")
    plt.ylabel("Number of facilities")
    plt.legend()

    plt.legend()
    plt.show()

def demand_curve(pstart, rate, sumt, timestep=12.0):
    pgrow = []
    for date in sumt:
        pgrow.append(pstart*((1.0+rate)**(date/timestep)))
        #print(date, timestep, pstart*((1.0+rate)**(date/timestep)))
    pgrow = np.asarray(pgrow)
    return pgrow

def calc_demand_error(pgrow, totalp):
    return np.sum(abs(pgrow-totalp)/pgrow)/len(pgrow)

def test_schedule(inputfile, parameters):
    facs, pstart, rate = parameters['facs'], parameters['pstart'], parameters['rate']
    prototypes, sim_length = read_file(inputfile)
    sumt, totalp = combine_power(prototypes, sim_length)
    pgrow = demand_curve(pstart, rate, sumt)
    diff = calc_demand_error(pgrow, totalp)
    return diff
