#!/usr/bin/env python3

##
# @file ramble_experiments.py
# @brief Script for experimenting with ramBLe.
# @author Ankit Srivastava <asrivast@gatech.edu>
#
# Copyright 2020 Georgia Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from collections import OrderedDict
from itertools import product
import os
from os.path import basename, isfile, join

from utils import get_hostfile, get_mpi_configurations, read_dataset, write_dataset, get_experiment_datasets, get_runtime


small_datasets = OrderedDict([
    #(name        , (-f, -n, -m, -s, -c, -v, -i)),
    ('lizards'    , ('test/lizards.csv', 3, 409, ',', False, True, False)),
    ('coronary'   , ('test/coronary.csv', 6, 1841, ',', False, True, False)),
    ('asia'       , ('test/asia.csv', 8, 5000, ',', False, True, False)),
    ('child'      , ('test/child.csv', 20, 10000, ' ', True, False, False)),
    ('insurance'  , ('test/insurance.csv', 27, 10000, ' ', True, False, False)),
    ('mildew'     , ('test/mildew.csv', 35, 10000, ' ', True, False, False)),
    ('alarm'      , ('test/alarm.csv', 37, 10000, ' ', True, False, False)),
    ])

big_datasets = OrderedDict([
    #(name        , (-f, -n, -m, -s, -c, -v, -i)),
    ('yeast'      , ('data/yeast/yeast_data_discretized.tsv', 5716, 2577, ' ', True, True, True)),
    ('development', ('data/athaliana/athaliana_development_discretized.tsv', 18373, 5102, ' ', True, True, True)),
    ('complete'   , ('data/athaliana/athaliana_complete_discretized.tsv', 18380, 16838, ' ', True, True, True)),
    ])

simulated_datasets = OrderedDict([
    #(name, (-f, -n, -m, -s, -c, -v, -i)),
    ('s1' , ('data/simulated/n30000_p0.00005_m10000_discretized.tsv', 30000, 10000, ' ', True, True, False)),
    ('s2' , ('data/simulated/n30000_p0.0001_m10000_discretized.tsv', 30000, 10000, ' ', True, True, False)),
    ('s3' , ('data/simulated/n30000_p0.0005_m10000_discretized.tsv', 30000, 10000, ' ', True, True, False)),
    ])

dataset_groups = dict([
    ('small',     small_datasets),
    ('big',       big_datasets),
    ('simulated', simulated_datasets),
    ])

all_datasets = OrderedDict(list(small_datasets.items()) + list(big_datasets.items()) + list(simulated_datasets.items()))

all_algorithms = [
    'gs',
    'iamb',
    'inter.iamb',
    'mmpc',
    'si.hiton.pc',
    'pc.stable',
    'pc.stable.2',
    ]

all_processes = [
    ]
for power in range(0, 11):
    all_processes.append(2 ** power)

NUM_REPEATS = 5


def parse_datasets(args):
    '''
    Get datasets to be used for the experiments.
    '''
    from os.path import splitext

    experiment_datasets = []
    if args.dataset is None:
        args.dataset = list(big_datasets.keys())
    for d in args.dataset:
        if d in all_datasets:
            experiment_datasets.append(d)
        elif d in dataset_groups:
            experiment_datasets.extend(list(dataset_groups[d].keys()))
        else:
            try:
                rd = read_dataset(d, args.separator, args.colobs, args.varnames, args.indices)
                m, n = rd.shape
                name = splitext(basename(d))[0]
                all_datasets[name] = (d, n, m, args.separator, args.colobs, args.varnames, args.indices)
                experiment_datasets.append(name)
            except:
                raise RuntimeError('Dataset %s is not recognized' % d)
    args.dataset = experiment_datasets


def parse_args():
    '''
    Parse command line arguments.
    '''
    import argparse
    from multiprocessing import cpu_count
    from os.path import expanduser, realpath

    parser = argparse.ArgumentParser(description='Run scaling experiments')
    parser.add_argument('--basedir', metavar='DIR', type=str, default=realpath(join(expanduser('~'), 'ramBLe')), help='Base directory for running the experiments')
    parser.add_argument('--scratch', metavar='DIR', type=str, default=realpath(join(expanduser('~'), 'scratch')), help='Scratch directory, visible to all the nodes')
    parser.add_argument('-d', '--dataset', metavar='NAME', type=str, nargs='*', help='Predefined dataset (or groups of datasets) or filename containing the dataset')
    parser.add_argument('-n', '--variables', metavar='N', type=int, nargs='*', help='Number of variable(s) to be used')
    parser.add_argument('-m', '--observations', metavar='M', type=int, nargs='*', help='Number of observation(s) to be used')
    parser.add_argument('-s', '--separator', type=str, metavar='DELIM', help='Delimiting character in the data set file')
    parser.add_argument('-c', '--colobs', action='store_true', help='The data set file contains observations in columns')
    parser.add_argument('-v', '--varnames', action='store_true', help='The data set file contains variable names')
    parser.add_argument('-i', '--indices', action='store_true', help='The data set file contains observation indices')
    parser.add_argument('-a', '--algorithm', metavar='NAME', type=str, nargs='*', default=all_algorithms, help='Algorithms to be used')
    parser.add_argument('-g', '--arguments', metavar='ARGS', type=str, help='Arguments to be passed to the underlying script')
    parser.add_argument('-u', '--undirected', action='store_true', help='Flag for generating undirected networks')
    parser.add_argument('-p', '--process', metavar='P', type=int, nargs='*', default=all_processes, help='Processes to be used')
    parser.add_argument('--ppn', metavar='PPN', type=int, nargs='*', default=[cpu_count()], help='Number of processes per node to be used')
    parser.add_argument('-r', '--repeat', metavar='N', type=int, default=NUM_REPEATS, help='Number of times the experiments should be repeated')
    parser.add_argument('--mpi-arguments', metavar='ARGS', type=str, help='Arguments to be passed to mpirun')
    parser.add_argument('--hostfile', metavar='HOSTS', type=str, help='Hostfile to be used for the runs')
    parser.add_argument('--bnlearn', action='store_true', help='Flag for running bnlearn instead of our implementation')
    parser.add_argument('--results', metavar = 'FILE', type=str, default='results_%s.csv' % os.environ.get('PBS_JOBID', 0), help='Name of the csv file to which results will be written')
    parser.add_argument('--suffix', type=str, default='', help='Suffix to add to the executable')
    parser.add_argument('--weak', metavar='N', type=int, nargs='*', help='Number of variables to be used on each processor')
    args = parser.parse_args()
    parse_datasets(args)
    if args.weak is not None and len(args.weak) != len(args.process):
        raise RuntimeError('Number of variables for weak scaling should be the same as the number of processes')
    return args


def get_executable_configurations(executable, datasets, algorithms, arguments, undirected, bnlearn):
    boolean_args = ['-c', '-v', '-i']
    default_ramble_args = ['-r', '--warmup', '--hostnames']
    configurations = []
    for name, algorithm in product(datasets, algorithms):
        dataset_args = all_datasets[name]
        script_args = [executable] + (['-d'] if not undirected else [])
        script_args.append('-a %s' % algorithm)
        script_args.append('-f %s -n %d -m %d -s \'%s\'' % tuple(dataset_args[:4]))
        script_args.extend(b for i, b in enumerate(boolean_args) if dataset_args[4 + i])
        if arguments is not None:
            script_args.append(arguments)
        if not bnlearn:
            script_args.extend(default_ramble_args)
        configurations.append((name, algorithm, ' '.join(script_args)))
    return configurations


def parse_runtimes(output):
    # optional runtimes
    warmup = get_runtime('warming up MPI', output, required=False)
    redistributing = get_runtime('redistributing', output, required=False)
    blankets = get_runtime('getting the blankets', output, required=False)
    symmetry = get_runtime('symmetry correcting the blankets', output, required=False)
    sync = get_runtime('synchronizing the blankets', output, required=False)
    neighbors = get_runtime('getting the neighbors', output, required=False)
    direction = get_runtime('directing the edges', output, required=False)
    gsquare = get_runtime('G-square computations', output, required=False)
    mxx = get_runtime('mxx calls', output, required=False)
    # required runtimes
    reading = get_runtime('reading the file', output, required=True)
    network = get_runtime('getting the network', output, required=True)
    writing = get_runtime('writing the network', output, required=True)
    return [warmup, reading, redistributing, blankets, symmetry, sync, neighbors, direction, mxx, gsquare, network, writing]


def run_experiment(basedir, scratch, config, undirected, repeat, bnlearn, compare):
    from datetime import datetime
    import subprocess
    import sys
    from tempfile import NamedTemporaryFile

    MAX_TRIES = 5
    dotfile = join(scratch, '%s_%s' % (config[0], config[1]))
    if undirected:
        dotfile += '_undirected'
    if bnlearn:
        dotfile += '_bnlearn'
    dotfile += '.dot'
    outfile = dotfile if not isfile(dotfile) else NamedTemporaryFile(suffix='.dot', dir=scratch, delete=False).name
    r = 0
    t = 0
    while r < repeat:
        arguments = config[-1] #+ ' -o %s' % outfile
        print('Started the run at', datetime.now().strftime('%c'))
        print(arguments)
        sys.stdout.flush()
        output = ''
        process = subprocess.Popen(arguments, shell=True, stdout=subprocess.PIPE)
        for line in iter(process.stdout.readline, b''):
            line = line.decode('utf-8')
            output += line
            print(line, end='')
        process.communicate()
        if process.returncode != 0:
            t += 1
            if t == MAX_TRIES:
                print('ERROR: Run failed %d times' % t)
                yield None
            print('Run failed. Retrying.')
            continue
        else:
            t = 0
        sys.stdout.flush()
        print('Finished the run at', datetime.now().strftime('%c'))
        print()
        if compare:
            print('Comparing generated file %s with %s' % (outfile, dotfile))
            sys.stdout.flush()
            compare_args = [join(basedir, 'common', 'scripts', 'compare_dot'), outfile, dotfile]
            try:
                subprocess.check_call(' '.join(compare_args), shell=True)
            except subprocess.CalledProcessError as ce:
                print(ce)
                print('ERROR: Comparison failed')
        yield parse_runtimes(output)
        r += 1


def get_weak_scaling_datasets(basedir, datasets, weak, scratch):
    if len(datasets) > 1:
        raise RuntimeError('Weak scaling with more than one data set is not yet supported')
    dname = datasets[0]
    dataset = all_datasets[dname]
    read = read_dataset(join(basedir, dataset[0]), dataset[3], dataset[4], dataset[5], dataset[6])
    weak_datasets = []
    for n in weak:
        dataset_n = list(dataset)
        dataset_n[0] = join(scratch, basename(dataset[0]) + '.' + str(n))
        dataset_n[1] = n
        write_dataset(read.iloc[:,:n], dataset_n[0], dataset_n[3], dataset_n[4], dataset_n[5], dataset_n[6])
        all_datasets.update([(dname + '.' + str(n), tuple(dataset_n))])
        weak_datasets.append(dname + '.' + str(n))
    return weak_datasets


def main():
    '''
    Main function.
    '''
    args = parse_args()
    datasets = args.dataset
    if args.variables or args.observations:
        datasets = get_experiment_datasets(args.basedir, datasets, args.variables, args.observations, args.scratch, all_datasets)
    elif args.weak:
        datasets = get_weak_scaling_datasets(args.basedir, datasets, args.weak, args.scratch)
    else:
        for dataset in datasets:
            ds = list(all_datasets[dataset])
            all_datasets[dataset] = tuple([join(args.basedir, ds[0])] + ds[1:]) if not isfile(ds[0]) else ds
    executable = join(args.basedir, 'ramble' + args.suffix) if not args.bnlearn else join(args.basedir, 'common', 'scripts', 'ramble_bnlearn.R')
    exec_configs = get_executable_configurations(executable, datasets, args.algorithm, args.arguments, args.undirected, args.bnlearn)
    if not args.bnlearn:
        mpi_configs = get_mpi_configurations(args.scratch, args.process, args.ppn, args.mpi_arguments, args.hostfile)
        if args.weak:
            all_configs = []
            i_m = 0
            while i_m != len(mpi_configs):
                i_d = 0
                while i_d != len(args.weak):
                    all_configs.extend((executable[0], executable[1], mpi[0], mpi[-1] + ' ' + executable[-1]) for executable, mpi in product(exec_configs[i_d*len(args.algorithm):(i_d+1)*len(args.algorithm)], mpi_configs[i_m:i_m+1]))
                    i_d += 1
                    i_m += 1
        else:
            all_configs = list((executable[0], executable[1], mpi[0], mpi[-1] + ' ' + executable[-1]) for executable, mpi in product(exec_configs, mpi_configs))
    else:
        all_configs = []
        for config, p, ppn in product(exec_configs, args.process, args.ppn):
            par_config = '--nprocs %d --ppn %d' % (p, ppn)
            all_configs.append(tuple(list(config[:-1]) + [p, config[-1] + ' ' + par_config]))
    print('*** Writing the results to', os.path.abspath(args.results), '***\n\n')
    with open(args.results, 'w') as results:
        results.write('# warmup,reading,redistributing,blankets,symmetry,sync,neighbors,direction,mxx,gsquare,network,writing\n')
        for config in all_configs:
            comment = 'runtime for dataset=%s using algorithm=%s on processors=%d' % tuple(config[:3])
            results.write('# %s %s\n' % ('our' if not args.bnlearn else 'bnlearn', comment))
            for rt in run_experiment(args.basedir, args.scratch, config, args.undirected, args.repeat, args.bnlearn, 0):
                if rt is not None:
                    results.write(','.join(str(t) for t in rt) + '\n')
                    results.flush()


if __name__ == '__main__':
    main()
