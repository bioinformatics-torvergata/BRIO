#!/usr/bin/env python
# coding: utf-8

###TO TEST - real files

#libraries

import re
import argparse

import numpy as np

from exceptions import *
#paths
mbr_path = "resources/mbr.csv"

#data
bear_string="abcdefghi=lmnopqrstuvwxyz^!\"#$%&\'()+234567890>[]:ABCDEFGHIJKLMNOPQRSTUVW{YZ~?_|/\\}@"

#argparse
parser = argparse.ArgumentParser(description='Look for motifs in database of motif PFMs')

parser.add_argument('--input','-i', dest='inputFile', action='store',
                    help='input multiFasta with BEAR notation')
parser.add_argument('--motifs','-m', dest='motifsFile', action='store',
                    help='target motifs file')
parser.add_argument('--sequence', dest='seqFlag', action='store_true',
                    help='for running the search on sequences instead of structures')
parser.add_argument('--output','-o', dest='output', action='store', default="stdout",
                    help='output file. Default: stdout')
args = parser.parse_args()

#read input
def parse_input(inputpath):
    seqs = {}
    seq_regex = re.compile("^[ACGTUacgtu]+$")
    db_regex = re.compile("^[\(\)\.]+$")
    counter = 0
    with open(inputpath) as f:
        line = f.readline().strip()
        while(line):
            if line.startswith(">"):
                #new sequence
                if counter:
                    seqs[name] = {'seq':seq,'db':db,'bear':bear,'counter':counter}
                counter += 1

                name = line
                seq = ""
                db = ""
                bear = ""

            elif seq_regex.match(line):
                seq += line
            elif db_regex.match(line):
                db += line
            else:
                #let's avoid a bear string regex
                bear += line

            line=f.readline().strip()
        seqs[name] = {'seq':seq,'db':db,'bear':bear,'counter':counter} 
    return seqs


#read motif data
def parse_name(line):
    """change as needed"""
    return line.strip()

def parse_motif(motifpath, seqFlag=False):
    if seqFlag:
        token = "#NT"
        antitoken = "#BEAR"
    else:
        token = "#BEAR"
        antitoken = "#NT"

    PSSM = {}
    with open(motifpath) as f:
        
        line= f.readline()
        while(line):
            if line.startswith("#NAME"):
                line = f.readline()
                name = parse_name(line)
                
                PSSM[name] = {}
            if line.startswith(antitoken):
                raise MotifGroupError("The parameters and the motif file specified do not match Guarracì!")
            if line.startswith(token):
                """get threshold score"""
                scores = []
                line=f.readline()
                while(line and line != "\n"):
                    scores.append(float(line.split()[5]))
                    line=f.readline()

                if scores:
                    thr = np.min(scores)
                else: thr = 9999    
                PSSM[name]['thr'] = thr

                
            if line.startswith("#PSSM"):
                line=f.readline()
                vals = []
                while(line and line != "\n"):
                    row = line.strip().split("\t")
                    vals.append({ pair[0] : float(pair[1:].split(":")[1].strip()) 
                                 for pair in row })
                    line=f.readline()
                    
                PSSM[name]['PSSM'] = vals
                
            line=f.readline()
    return PSSM


#read MBR
def read_MBR(mbr_path, size = 83):
    return np.fromfile(mbr_path, sep=",").reshape(size,size)


def compare(rna, motifs, mbr, bear_string, seqFlag=False):
    """scores one rna against all motifs
    rna: string
    motifs: dictionary -- motifs[name][thr/PSSM]"""
    results = {}
    for motif in motifs:
        thr = motifs[motif]['thr']
        motif_size = len(motifs[motif]['PSSM'])            
        best_score, position = score(rna, motifs[motif]['PSSM'], motif_size, mbr, bear_string, seqFlag)
        results[motif] = (best_score, thr, position, motif_size)
        
    return results

def score(rna, pssm, motif_size, mbr, bear_string, seqFlag = False, match=3, mismatch=-2):
    """tests all possible ungapped alignments"""
    best_score= -9999
    position=-1
    rna_len = len(rna)
    if rna_len >= motif_size:
        for start in range(0, rna_len-motif_size+1):
            slice_score = 0.0
            for b_rna, b_list in zip(rna[start:start+motif_size],pssm):
                position_score = 0.0
                for b_char in b_list:
                    #frequency * subs(i,j)
                    if not seqFlag:
                        position_score += b_list[b_char] * mbr[ bear_string.index(b_char), bear_string.index(b_rna) ]
                    else:     
                        position_score += b_list[b_char] * (match if b_char == b_rna else mismatch)
                slice_score += position_score
            if slice_score > best_score:
                best_score = slice_score
                position = start
    else:
        for start in range(0, -rna_len+motif_size+1):
            slice_score = 0.0
            for b_rna, b_list in zip(rna,pssm[start:start+rna_len]):
                position_score = 0.0
                for b_char in b_list:
                    #frequency * subs(i,j)
                    if not seqFlag:
                        position_score += b_list[b_char] * mbr[ bear_string.index(b_char), bear_string.index(b_rna) ]
                    else:     
                        position_score += b_list[b_char] * (match if b_char == b_rna else mismatch)
                    
                slice_score += position_score
            if slice_score > best_score:
                best_score = slice_score
                position = start
                
    return best_score,position
    


seqs = parse_input(args.inputFile)
motifs = parse_motif(args.motifsFile, args.seqFlag)
print(motifs)

for name in seqs:
    if args.seqFlag:
        focus = 'seq'
    else:
        focus = 'bear'
    to_align = seqs[name][focus]
    out = compare(to_align, motifs, read_MBR(mbr_path), bear_string, args.seqFlag)
    if args.output == 'stdout':
        print(out)
    else:
        with open(args.output, 'w') as f:
            print(out, file=f)




