'''
It is assumed that the input elements (in sys.argv[1] and sys.argv[2]) are:
>header
RNA sequence

or

>header
RNA sequence
Dot-Bracket structure
'''
import sys
import os
import subprocess
import re

from random import choice
from string import ascii_uppercase

import scipy.stats as stats

outer = re.compile(" (.+)$")

def run_search(dir_base, path_motif, path_input_seq_struct_bear, str_else_nuc, path_output):
    subprocess.Popen(
        [
            'python3', os.path.join(dir_base, 'scripts', 'search2.0.py'),
            '--input', path_input_seq_struct_bear,
            '--motifs', path_motif,
            '--output', path_output
        ] + ([] if str_else_nuc else ['--sequence'])
        ,
        # To get strings
        universal_newlines=True
    ).wait()

def perc_seq_motif(motif, inp_search,dic, str_else_nuc):
    #num seq col motivo
    major=0
    #num seq senza motivo
    minor=0

    tot=0
    threshold=dic[motif]

    f = inp_search.strip('\n').split('\n')
    if str_else_nuc:
        for line in f:
            line = line.split('\t')
            if len(line)>2:
                tot=tot+1
                val=float(line[3].strip('\n'))
                if val>threshold:
                    major=major+1
    else:
        for line in f:
            tot=tot+1
            val=float(line.split('\t')[2])
            if val>threshold:
                major=major+1

    if tot==0:
        perc=0
    else:
        perc=float(major)/tot*100   
        minor=tot-major

    return (perc, major, minor)

def Search_motif_name(file_bench):
    f=open(file_bench)
    line=f.readline()
    pssm=[]
    while(line):
        if line=="#PSSM\n":
            pssm.append(line.split())
            while (line[0:6] != "#score"):
                line=f.readline()
                pssm.append(line.split())

        line=f.readline()
    f.close()
    
    m=[el[0] for el in pssm[1:-2]]
    motif_name=''.join(m)

    return motif_name

def process_input_rna_molecules(input_rna_molecules, dir_output):
    missing_dotbracket_and_bear_rna_molecules = ''
    missing_bear_rna_molecules = ''

    input_rna_to_length_dict = {}

    max_rna_seq_len = 3000 if len(input_rna_molecules.split('\n>')) < 1000 else 500
    removed_too_long_rna_molecules = ''
    for single_rna in input_rna_molecules.strip('\n>').split('\n>'):
        single_rna_list = [x.strip('\r') for x in single_rna.split('\n')]

        single_rna_list[1] = single_rna_list[1].upper().replace('T', 'U')

        single_rna_list[0] = '>' + single_rna_list[0] 
        if len(single_rna_list[1]) > max_rna_seq_len:
            removed_too_long_rna_molecules += '\n'.join(single_rna_list) + '\n'
        else:
            input_rna_to_length_dict[single_rna_list[0]] = len(single_rna_list[1])

            if len(single_rna_list) == 2:
                missing_dotbracket_and_bear_rna_molecules += '\n'.join(single_rna_list) + '\n'
            else:
                missing_bear_rna_molecules += '\n'.join(single_rna_list) + '\n'

    path_complete_input = os.path.join(dir_output, 'tmp.complete_input_with_dot_bracket_and_bear.txt')

    missing_bear_rna_molecules_all = ''
    if missing_dotbracket_and_bear_rna_molecules:
        path_missing_dot_bracket_input = os.path.join(dir_output, 'tmp.missing_dot_bracket_input.txt')
        with open(path_missing_dot_bracket_input, 'w') as fw:
            fw.write(missing_dotbracket_and_bear_rna_molecules)

        # Calculate dotbracket
        missing_bear_rna_molecules_added_dot_bracket = subprocess.check_output(
            [os.path.join(dir_base, 'scripts', 'RNAfold'), '--noPS', path_missing_dot_bracket_input],
            # To get strings
            universal_newlines=True
        )

        # Remove the energies
        for x in missing_bear_rna_molecules_added_dot_bracket.strip('\n>').split('\n>'):
            x_list = x.split('\n')
            x_list[2] = re.sub(r' \((.*?)\)', '', x_list[2])
            missing_bear_rna_molecules_all += '>' +'\n'.join(x_list) + '\n'

    missing_bear_rna_molecules_all += missing_bear_rna_molecules
    if missing_bear_rna_molecules_all:
        path_missing_bear_input = os.path.join(dir_output, 'tmp.missing_bear_input.txt')
        with open(path_missing_bear_input, 'w') as fw:
            fw.write(missing_bear_rna_molecules_all)

        # Calculate BEAR
        subprocess.call(
            ['java', '-jar', os.path.join(dir_base, 'scripts', 'BearEncoder_new.jar'), path_missing_bear_input, path_complete_input]
        )

    return path_complete_input, input_rna_to_length_dict


dir_base = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

dir_struct_motifs = os.path.join(dir_base, 'motifs_str_groups/')
dir_nucleotide_motifs = os.path.join(dir_base, 'motifs_nuc_groups/')

is_there_a_background = sys.argv[2]

# To get from user input?
search_struct_motifs = 'str' #else ''
search_seq_motifs = 'nuc' #else ''

user_id = sys.argv[3]

dir_user = os.path.join(dir_base, 'results', user_id)


# Directory preparation
if not os.path.exists(dir_user):
    os.makedirs(dir_user)

path_complete_input_rna_molecules, input_rna_to_length_dict = process_input_rna_molecules(sys.argv[1], dir_user)

path_complete_input_rna_molecules_background = ''
if is_there_a_background:
    if not os.path.exists(os.path.join(dir_user, 'background')):
        os.makedirs(os.path.join(dir_user, 'background'))

    path_complete_input_rna_molecules_background, _ = process_input_rna_molecules(sys.argv[2], os.path.join(dir_user, 'background'))


species_list = sys.argv[4].split(',')
experiments_list = sys.argv[5].split(',')

if not is_there_a_background:
    #creo dizionario per bg: chiave=nome, lista=[major, minor]
    f=open(os.path.join(dir_base, 'resources', 'summary_AutoBg.txt'))
    line=f.readline()
    dict_bg={}
    while (line):
        dict_bg[line.split()[0]]=[int(line.split()[2]),int(line.split()[3])]
        line=f.readline()
    f.close()

import re
for str_or_nuc, dir_str_or_nuc_motifs in zip(
    [search_struct_motifs, search_seq_motifs],
    [dir_struct_motifs, dir_nucleotide_motifs],
):
    if str_or_nuc:
        input_or_background_to_result_to_output_dict = {}
        # For input and (eventually) the background
        for path_complete_input_rna_molecules_xxx, input_or_background in zip(
            [path_complete_input_rna_molecules, path_complete_input_rna_molecules_background],
            ['input', 'background']
        ):
            # The background path can be empty
            if path_complete_input_rna_molecules_xxx:
                for filename_motif in [x for x in os.listdir(dir_str_or_nuc_motifs) if x.startswith('motifs_')]:
                    experiment, specie = filename_motif.split('_')[1:3]

                    if re.findall(r"(?=("+'|'.join(species_list)+r"))", specie) and re.findall(r"(?=("+'|'.join(experiments_list)+r"))", experiment):                        
                        path_str_or_nuc_search_out = os.path.join(dir_user, 'search_out.{}.txt'.format(filename_motif.split(".")[0]))
                        run_search(
                            dir_base,
                            os.path.join(dir_str_or_nuc_motifs, filename_motif),
                            path_complete_input_rna_molecules_xxx,
                            str_or_nuc == 'str',
                            path_str_or_nuc_search_out
                        )

# To remove temporary files (path_missing_dot_bracket_input, path_missing_bear_input, ...)

for path_tmp_file in [os.path.join(dir_user, x) for x in os.listdir(dir_user) if x.startswith('tmp.')]:
    print('Remove', path_tmp_file)
    os.remove(path_tmp_file)

with open(os.path.join(dir_user, 'Out.log'), 'w') as fw:
    fw.write('done')
    # This log file could be used to write something during the searches to estimate the remaining time
