#!/usr/bin/env python
# coding: utf-8

# libraries
import re
import argparse
import json

from exceptions import *

# paths
mbr_path = "resources/MBR.tsv"

# argparse
parser = argparse.ArgumentParser(description='Look for motifs in database of motif PFMs')

parser.add_argument('--input', '-i', dest='inputFile', action='store',
                    help='input multiFasta with BEAR notation')
parser.add_argument('--motifs', '-m', dest='motifsFile', action='store',
                    help='target motifs file')
parser.add_argument('--sequence', dest='seqFlag', action='store_true',
                    help='for running the search on sequences instead of structures')
parser.add_argument('--output', '-o', dest='output', action='store', default="stdout",
                    help='output file. Default: stdout')
args = parser.parse_args()


def parse_input(inputpath):
    seqs = {}
    seq_regex = re.compile("^[ACGTUacgtu]+$")
    db_regex = re.compile("^[\(\)\.]+$")
    counter = 0
    with open(inputpath) as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                # new sequence

                if counter > 0:
                    # Save the previous sequence
                    seqs[name] = {'seq': seq, 'db': db, 'bear': bear, 'counter': counter}

                name = line
                seq = ""
                db = ""
                bear = ""

                counter += 1
            elif seq_regex.match(line):
                seq += line
            elif db_regex.match(line):
                db += line
            else:
                # let's avoid a bear string regex
                bear += line

        # Last sequence
        seqs[name] = {'seq': seq, 'db': db, 'bear': bear, 'counter': counter}

    return seqs


def parse_motif(motifpath, seq_flag=False):
    if seq_flag:
        token = "#NT"
        antitoken = "#BEAR"
    else:
        token = "#BEAR"
        antitoken = "#NT"

    motif_info = {}
    with open(motifpath) as f:
        line = f.readline()
        while line:
            if line.startswith("#NAME"):
                name = f.readline().strip()

                motif_info[name] = {}
            if line.startswith(antitoken):
                raise MotifGroupError("The parameters and the motif file specified do not match!")
            if line.startswith(token):
                """get threshold score"""
                line = f.readline()
                thr = 9999
                while line and line != "\n":
                    current_score = float(line.split()[5])
                    if current_score < thr:
                        thr = current_score
                    line = f.readline()

                motif_info[name]['thr'] = thr

            if line.startswith("#PSSM"):
                line = f.readline()
                vals = []
                while line and line != "\n":
                    row = line.strip().split("\t")
                    vals.append({
                        pair[0]: float(pair[1:].split(":")[1].strip()) for pair in row
                    })
                    line = f.readline()

                motif_info[name]['PSSM'] = vals

            line = f.readline()

    return motif_info


def read_MBR(mbr_path):
    mbr_dict = {}
    with open(mbr_path) as f:
        header_list = f.readline().rstrip().split('\t')[1:]

        for line in f:
            splitted = line.strip().split('\t')

            mbr_dict[splitted[0]] = {char: float(score) for char, score in zip(header_list, splitted[1:])}

    return mbr_dict


def compare(rna, motifs, mbr_dict, seq_flag=False):
    """
    Scores one RNA against all motifs
    rna: string (primary sequence or bear string)
    motifs: dictionary -- motifs[name][thr and PSSM]
    """

    results = {}
    for motif_name, info_motif in motifs.items():
        motif_size = len(info_motif['PSSM'])
        best_score, position = score(rna, info_motif['PSSM'], motif_size, mbr_dict, seq_flag)

        if position >= 0:
            results[motif_name] = (best_score, info_motif['thr'], position, motif_size)

    return results


def score(rna, pssm, motif_size, mbr_dict, seq_flag=False, match=3, mismatch=-2):
    """
    tests all possible ungapped alignments
    """

    best_score = -9999
    position = -1
    rna_len = len(rna)
    if rna_len >= motif_size:
        for start in range(0, rna_len - motif_size + 1):
            slice_score = 0.0
            for b_rna, b_dict in zip(rna[start:(start + motif_size)], pssm):
                position_score = 0.0

                # frequency * subs(i,j)
                if not seq_flag:
                    mbr_row_dict = mbr_dict[b_rna]

                    for b_char, sos_score in b_dict.items():
                        position_score += sos_score * mbr_row_dict[b_char]
                else:
                    for b_char, sos_score in b_dict.items():
                        position_score += sos_score * (match if b_char == b_rna else mismatch)

                slice_score += position_score

            if slice_score > best_score:
                best_score = slice_score
                position = start
    # else:
    #    for start in range(0, motif_size - rna_len + 1):
    #        slice_score = 0.0
    #        for b_rna, b_list in zip(rna, pssm[start:(start + rna_len)]):
    #            index_b_rna = bear_dict[b_rna]
    #
    #            position_score = 0.0
    #            for b_char in b_list:
    #                # frequency * subs(i,j)
    #                if not seq_flag:
    #                    position_score += b_list[b_char] * mbr[bear_dict[b_char], index_b_rna]
    #                else:
    #                    position_score += b_list[b_char] * (match if b_char == b_rna else mismatch)
    #
    #            slice_score += position_score
    #
    #        if slice_score > best_score:
    #            best_score = slice_score
    #            position = start

    return best_score, position


seqs = parse_input(args.inputFile)
motifs = parse_motif(args.motifsFile, args.seqFlag)
# print(seqs)
# print(motifs)

string_to_align = 'seq' if args.seqFlag else 'bear'

mbr_np = read_MBR(mbr_path)

seq_to_result = {}

for seq_name, info in seqs.items():
    seq_to_result[seq_name] = compare(info[string_to_align], motifs, mbr_np, args.seqFlag)

if args.output == 'stdout':
    json.dump(seq_to_result, sys.stdout)
else:
    with open(args.output, 'w') as f:
        json.dump(seq_to_result, f)
