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

dir_base = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

dir_user = os.path.join(dir_base, 'results',
    ''.join(choice(ascii_uppercase) for i in range(20))
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

    # Calculate dotbracket: do I have to wait? It is a blocking call
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