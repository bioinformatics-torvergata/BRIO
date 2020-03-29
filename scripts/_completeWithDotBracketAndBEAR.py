'''
It is assumed that the input elements (in sys.argv[1]) are:
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

DIR_STRUCT_MOTIFS = '/home/andrea/Scrivania/motifs_str/'
DIR_NUCLEOTIDE_MOTIFS = '/home/andrea/Scrivania/motifs_nuc/'

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



dir_base = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

dir_user = os.path.join(dir_base, 'results',
    ''.join(choice(ascii_uppercase) for i in range(32))
)
outer = re.compile(" (.+)$")

missing_dotbracket_and_bear_rna_molecules = ''
missing_bear_rna_molecules = ''

max_rna_seq_len = 3000 if len(sys.argv[1].split('\n>')) < 1000 else 500
removed_too_long_rna_molecules = ''

for single_rna in sys.argv[1].strip('\n>').split('\n>'):
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

if not os.path.exists(dir_user):
    os.makedirs(dir_user)

path_complete_input = os.path.join(dir_user, 'tmp.complete_input_with_dot_bracket_and_bear.txt')

missing_bear_rna_molecules_all = ''
if missing_dotbracket_and_bear_rna_molecules:
    path_missing_dot_bracket_input = os.path.join(dir_user, 'tmp.missing_dot_bracket_input.txt')
    with open(path_missing_dot_bracket_input, 'w') as fw:
        fw.write(missing_dotbracket_and_bear_rna_molecules)

    # Calculate dotbracket
    missing_bear_rna_molecules_added_dot_bracket = subprocess.check_output(
        [os.path.join(dir_base, 'scripts', 'RNAfold'), '--noPS', path_missing_dot_bracket_input]
    )

    # Remove the energies
    for x in missing_bear_rna_molecules_added_dot_bracket.strip('\n>').split('\n>'):
        x_list = x.split('\n')
        x_list[2] = re.sub(r' \((.*?)\)', '', x_list[2])
        missing_bear_rna_molecules_all += '>' +'\n'.join(x_list) + '\n'

missing_bear_rna_molecules_all += missing_bear_rna_molecules
if missing_bear_rna_molecules_all:
    path_missing_bear_input = os.path.join(dir_user, 'tmp.missing_bear_input.txt')
    with open(path_missing_bear_input, 'w') as fw:
        fw.write(missing_bear_rna_molecules_all)

    # Calculate BEAR
    subprocess.call(
        ['java', '-jar', os.path.join(dir_base, 'scripts', 'BearEncoder_new.jar'), path_missing_bear_input, path_complete_input]
    )

dir_user_output_str = os.path.join(dir_user, 'out_search_str')
if not os.path.exists(dir_user_output_str):
    os.makedirs(dir_user_output_str)

for filename_motif in os.listdir(DIR_STRUCT_MOTIFS):
    path_str_output = os.path.join(dir_user_output_str, filename_motif.split('.')[0] + '_out_search.str.txt')
    # os.system('cp -R /home/sangiovanni/public_html/brio/motifs_logo/str/ '+folder+'/logos/')
    run_search(dir_base, os.path.join(DIR_STRUCT_MOTIFS, filename_motif), path_complete_input, True, path_str_output)
    break


dir_user_output_nuc = os.path.join(dir_user, 'out_search_nuc')
if not os.path.exists(dir_user_output_nuc):
    os.makedirs(dir_user_output_nuc)

for filename_motif in os.listdir(DIR_NUCLEOTIDE_MOTIFS):
    path_str_output = os.path.join(dir_user_output_nuc, filename_motif.split('.')[0] + '_out_search.nuc.txt')
    # os.system('cp -R /home/sangiovanni/public_html/brio/motifs_logo/nuc/ '+folder+'/logos/')
    run_search(dir_base, os.path.join(DIR_NUCLEOTIDE_MOTIFS, filename_motif), path_complete_input, False, path_str_output)
    break










print('END')

# To delete path_missing_dot_bracket_input path_missing_bear_input
