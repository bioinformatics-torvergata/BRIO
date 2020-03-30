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
    if str_else_nuc:
        with open(path_output, 'w') as output_file:
            subprocess.call(
                [
                    'java', '-jar', os.path.join(dir_base, 'scripts', 'search1.2.jar'),
                    path_motif,
                    path_input_seq_struct_bear
                ],
                stdout=output_file
            )
    else:
        subprocess.call(
            [
                'python3', os.path.join(dir_base, 'scripts', 'Search_nt.py'),
                path_motif,
                path_input_seq_struct_bear,
                path_output
            ]
        )

def perc_seq_motif(motif, inp_search,dic, str_else_nuc):
    #num seq col motivo
    major=0
    #num seq senza motivo
    minor=0

    tot=0
    threshold=dic[motif]

    f=open(inp_search,'r').readlines()
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

    max_rna_seq_len = 3000 if len(input_rna_molecules.split('\n>')) < 1000 else 500
    removed_too_long_rna_molecules = ''

    for single_rna in input_rna_molecules.strip('\n>').split('\n>'):
        single_rna_list = [x.strip('\r') for x in single_rna.split('\n')]
        single_rna_list[1] = single_rna_list[1].upper().replace('T', 'U')

        single_rna_list[0] = '>' + single_rna_list[0] 
        if len(single_rna_list[1]) > max_rna_seq_len:
            removed_too_long_rna_molecules += '\n'.join(single_rna_list) + '\n'
        else:
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
        print('MIAO2', missing_bear_rna_molecules_added_dot_bracket, 'asdsada', str(missing_bear_rna_molecules_added_dot_bracket).strip('\n>'))

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

    return path_complete_input


dir_base = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

dir_struct_motifs = os.path.join(dir_base, 'some_motifs_str/')
dir_nucleotide_motifs = os.path.join(dir_base, 'some_motifs_nuc/')

is_there_a_background = sys.argv[2]

dir_user = os.path.join(dir_base, 'results',
    ''.join(choice(ascii_uppercase) for i in range(32))
)

if not os.path.exists(dir_user):
    os.makedirs(dir_user)


path_complete_input_rna_molecules = process_input_rna_molecules(sys.argv[1], dir_user)
dir_user_output_str = os.path.join(dir_user, 'out_search_str')
dir_user_output_nuc = os.path.join(dir_user, 'out_search_nuc')

path_complete_input_rna_molecules_background = ''
dir_user_output_str_background = ''
dir_user_output_nuc_background = ''
if is_there_a_background:
    if not os.path.exists(os.path.join(dir_user, 'background')):
        os.makedirs(os.path.join(dir_user, 'background'))

    path_complete_input_rna_molecules_background = process_input_rna_molecules(sys.argv[2], os.path.join(dir_user, 'background'))
    dir_user_output_str_background = os.path.join(dir_user, 'background', 'out_search_str')
    dir_user_output_nuc_background = os.path.join(dir_user, 'background', 'out_search_nuc')

# Structure motifs
for path_complete_input_rna_molecules_xxx, dir_user_output_str_xxx in zip(
    [path_complete_input_rna_molecules, path_complete_input_rna_molecules_background],
    [dir_user_output_str, dir_user_output_str_background]
):
    if path_complete_input_rna_molecules_xxx:
        print('dir_user_output_str', dir_user_output_str_xxx)

        if not os.path.exists(dir_user_output_str_xxx):
            os.makedirs(dir_user_output_str_xxx)

        for filename_motif in os.listdir(dir_struct_motifs):
            path_str_output = os.path.join(dir_user_output_str_xxx, filename_motif.split('.')[0] + '_out_search.str.txt')
            # os.system('cp -R /home/sangiovanni/public_html/brio/motifs_logo/str/ '+folder+'/logos/')
            run_search(dir_base, os.path.join(dir_struct_motifs, filename_motif), path_complete_input_rna_molecules_xxx, True, path_str_output)


# To load this one-time only when the server starts(?)
struct_motif_dict = {}
with open(os.path.join(dir_base, 'resources', 'dict_str.txt')) as f:
    for line in f:
        key, value = line.strip('\n').split('\t')
        struct_motif_dict[key]=float(value)

to_write = ''
for name_result in os.listdir(dir_user_output_str):
    motif_key = name_result.split('_out_')[0]+'.txt'
    path_result = os.path.join(dir_user_output_str, name_result)

    perc, major, minor = perc_seq_motif(motif_key, path_result, struct_motif_dict, True)

    if is_there_a_background:
        perc_bg, major_bg, minor_bg = perc_seq_motif(motif_key, path_result, struct_motif_dict, True)
    else:
        #creo dizionario per bg: chiave=nome, lista=[major, minor]
        f=open(os.path.join(dir_base, 'resources', 'summary_AutoBg.txt'))
        line=f.readline()
        dict_bg={}
        while (line):
            dict_bg[line.split()[0]]=[int(line.split()[2]),int(line.split()[3])]
            line=f.readline()
        f.close()
        
        major_bg=dict_bg[motif_key][0]
        minor_bg=dict_bg[motif_key][1]

    #calcolo fisher test
    oddsratio, pvalue = stats.fisher_exact([[major, major_bg], [minor, minor_bg]])

    motif_name = Search_motif_name(os.path.join(dir_struct_motifs, motif_key))
    regione = str(motif_key.split('_')[-3])
    n_motif = str(motif_key.split('_')[-2])
    RBP_name = str(motif_key.split('_')[1])
    #scrivo modello, regione, numero motivo, perc|oddsratio|p-value, nome del file con i risultati (che potra' essere scaricato), nome rbp
    to_write += motif_name+"\t"+regione+"\t"+n_motif+"\t"+str(round(perc,2))+"|"+str(round(oddsratio,2))+"|"+str(pvalue)+"\t"+motif_key+"\t"+RBP_name+"\n"


    with open(os.path.join(dir_user, 'tmp.search_out_no_domains.txt'), 'a') as f:
        f.write(to_write)

'''
# Nucleotide motifs
dir_user_output_nuc = os.path.join(dir_user, 'out_search_nuc')
if not os.path.exists(dir_user_output_nuc):
    os.makedirs(dir_user_output_nuc)

for filename_motif in os.listdir(dir_nucleotide_motifs):
    path_str_output = os.path.join(dir_user_output_nuc, filename_motif.split('.')[0] + '_out_search.nuc.txt')
    # os.system('cp -R /home/sangiovanni/public_html/brio/motifs_logo/nuc/ '+folder+'/logos/')
    run_search(dir_base, os.path.join(dir_nucleotide_motifs, filename_motif), path_complete_input, False, path_str_output)
    break

if is_there_a_background:
    pass # TO DO


#complete_search.py dir_user
'''




print('END')

# To delete path_missing_dot_bracket_input path_missing_bear_input
