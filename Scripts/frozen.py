# -*- coding: utf-8 -*-
"""
@author: SASWATA DASGUPTA
"""
import numpy as np
import os
import sys


def read_lines(filename):
    """
    Read file line by line using a generator expression
    """
    with open(filename, "r") as f:
        yield from f.readlines()


if __name__ == "__main__":
    # Handle command-line arguments
    try:
        infile = sys.argv[1]
    except IndexError:
        print("Usage: python frozen.py <input_file> <opt/ts>")
        sys.exit(1)

frz_conf = list(read_lines("frozen.txt"))
conf_atoms = frz_conf[1].strip()
At = np.array(list(map(int, conf_atoms.split())))


with open('frozen.txt', 'r') as input_file:
    frozen_opt = []

    for line in input_file:
        if line.startswith('$frozen_opt'):
            for line in input_file:
                if line.startswith('$end'):
                    break
                frozen_opt.extend(line.split())

    with open('frozen_fm.txt', 'w') as output_file:
        output_file.write('$opt\nFIXED\n')
        for option in frozen_opt:
            output_file.write(f'{option:<4}XYZ\n')
        output_file.write('ENDFIXED\n')
        output_file.write('$end\n') 


mol_label_opt='''
$molecule
0 1
'''

rem_opt='''
$end

$rem
method b3lyp
basis  6-31G(d,p)
jobtype opt
GEOM_OPT_MAX_CYCLES 1500
DFT_D D3_BJ
SYMMETRY             false
SYM_IGNORE           true
NO_REORIENT          true
MEM_TOTAL 60000
$end
'''

block_freq='''
@@@@

$molecule
read
$end

$rem
method b3lyp
basis  6-31G(d,p)
jobtype freq
DFT_D D3_BJ
FRZN_OPT 1
FRZ_ATOMS {}
SYMMETRY             false
SYM_IGNORE           true
NO_REORIENT          true
MEM_TOTAL 60000
$end
'''.format(At.shape[0])

ts_freq='''
$end

$rem
method b3lyp
basis  6-31G(d,p)
jobtype freq
DFT_D D3_BJ
SYMMETRY             false
SYM_IGNORE           true
NO_REORIENT          true
MEM_TOTAL 60000
$end

@@@

$molecule
read
$end

$rem
method b3lyp
basis  6-31G(d,p)
jobtype ts
SCF_GUESS            read
GEOM_OPT_DMAX        100
GEOM_OPT_MAX_CYCLES 1500
SYMMETRY             false
GEOM_OPT_HESSIAN     read
SYM_IGNORE           true
NO_REORIENT          true
MEM_TOTAL 60000
$end
'''

if sys.argv[2] == "opt":
    with open(infile[:-4]+".inp", 'w') as f:
        f.write(mol_label_opt)
        with open(infile, 'r') as fp:
            lines = fp.readlines()
            for i in lines:
                f.write(i)
        f.write(rem_opt)
        f.write("\n")
        with open("frozen_fm.txt", 'r') as fc:
            lines_coord = fc.readlines()
            for k in lines_coord:
                f.write(k)
        f.write(block_freq)
        f.write("\n")
        with open("frozen.txt", 'r') as fx:
             lines_frz = fx.readlines()
             for j in lines_frz:
                   f.write(j)
        f.write("\n")

if sys.argv[2] == "ts":
    with open(infile[:-4] + ".inp", 'w') as f:
        f.write(mol_label_opt)
        with open(infile, 'r') as fp:
            lines = fp.readlines()
            for i in lines:
                f.write(i)
        f.write(ts_freq)
        f.write("\n")
        with open("frozen_fm.txt", 'r') as fc:
            lines_coord = fc.readlines()
            for k in lines_coord:
                f.write(k)
        f.write(block_freq)
        f.write("\n")
        with open("frozen.txt", 'r') as fx:
             lines_frz = fx.readlines()
             for j in lines_frz:
                   f.write(j)
        f.write("\n")
        f.close()


os.remove("frozen_fm.txt")
