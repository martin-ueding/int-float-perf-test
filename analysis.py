#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2015 Martin Ueding <dev@martin-ueding.de>

import argparse
import re

import numpy as np
import matplotlib.pyplot as pl

def get_cpu_name():
    with open('/proc/cpuinfo') as f:
        for line in f:
            if line.startswith('model name'):
                parts = line.split(':')

                return parts[1].strip()

def main():
    options = _parse_args()

    pattern = re.compile(r'data-(.*).txt')

    fig = pl.figure()
    ax = fig.add_subplot(1, 1, 1)

    fig2 = pl.figure()
    ax2 = fig2.add_subplot(1, 1, 1)

    for filename in options.filename:
        data = np.loadtxt(filename)
        cores = data[:, 0]
        duration = data[:, 1]

        efficiency = duration[0] / duration
        speedup = cores * duration[0] / duration

        m = pattern.match(filename)
        assert m
        label = m.group(1)

        ax.plot(cores, efficiency, label=label, marker='o')
        ax2.plot(cores, speedup, label=label, marker='o')

    if options.cpu is None:
        cpu_name = get_cpu_name()
    else:
        cpu_name = options.cpu

    x = np.linspace(1, np.max(cores) / 2, 2)
    y = np.ones(x.shape)
    ax.plot(x, y, color='black')
    y = x
    ax2.plot(x, y, color='black')

    ax.set_title('Replicated Fibonacci on {}'.format(cpu_name))
    ax.set_xlabel('Threads')
    ax.set_ylabel('Efficiency')
    #ax.set_xscale('log', basex=2)
    ax.grid(True)
    ax.legend(loc='best')
    ax.margins(0.05)
    fig.tight_layout()
    fig.savefig('efficiency.pdf')
    fig.savefig('efficiency.svg')

    ax2.set_title('Replicated Fibonacci on {}'.format(cpu_name))
    ax2.set_xlabel('Threads')
    ax2.set_ylabel('Speedup')
    #ax.set_xscale('log', basex=2)
    ax2.grid(True)
    ax2.legend(loc='best')
    ax2.margins(0.05)
    fig2.tight_layout()
    fig2.savefig('speedup.pdf')
    fig2.savefig('speedup.svg')

def _parse_args():
    '''
    Parses the command line arguments.

    :return: Namespace with arguments.
    :rtype: Namespace
    '''
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('filename', nargs='+')
    parser.add_argument('--cpu')
    options = parser.parse_args()

    return options

if __name__ == '__main__':
    main()
