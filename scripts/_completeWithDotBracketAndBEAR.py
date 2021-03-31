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

import output_generation

from random import choice
from string import ascii_uppercase

import scipy.stats as stats

import json

outer = re.compile(" (.+)$")


def run_search(dir_base, path_motif, path_input_seq_struct_bear, str_else_nuc, path_output):
    subprocess.Popen(
        [
            'python3', os.path.join(dir_base, 'scripts', 'search2.0.py'),
            '--input', path_input_seq_struct_bear,
            '--motifs', path_motif,
            '--output', path_output
        ] + ([] if str_else_nuc else ['--sequence']),
        # To get strings
        universal_newlines=True
    ).wait()


def perc_seq_motif(motif, inp_search, dic, str_else_nuc):
    # num seq col motivo
    major = 0
    # num seq senza motivo
    minor = 0

    tot = 0
    threshold = dic[motif]

    f = inp_search.strip('\n').split('\n')
    if str_else_nuc:
        for line in f:
            line = line.split('\t')
            if len(line) > 2:
                tot = tot + 1
                val = float(line[3].strip('\n'))
                if val > threshold:
                    major = major + 1
    else:
        for line in f:
            tot = tot + 1
            val = float(line.split('\t')[2])
            if val > threshold:
                major = major + 1

    if tot == 0:
        perc = 0
    else:
        perc = float(major) / tot * 100
        minor = tot - major

    return perc, major, minor


def search_motif_name(file_bench):
    f = open(file_bench)
    line = f.readline()
    pssm = []
    while line:
        if line == "#PSSM\n":
            pssm.append(line.split())
            while line[0:6] != "#score":
                line = f.readline()
                pssm.append(line.split())

        line = f.readline()

    f.close()

    m = [el[0] for el in pssm[1:-2]]
    motif_name = ''.join(m)

    return motif_name


def process_input_rna_molecules(input_rna_molecules, dir_output):
    missing_dotbracket_and_bear_rna_molecules = ''
    missing_bear_rna_molecules = ''

    input_rna_to_length_dict = {}

    for single_rna in input_rna_molecules.strip('\n>').split('\n>'):
        single_rna_list = [x.strip('\r') for x in single_rna.split('\n')]

        single_rna_list[0] = '>' + single_rna_list[0]
        single_rna_list[1] = single_rna_list[1].upper().replace('T', 'U')

        input_rna_to_length_dict[single_rna_list[0]] = len(single_rna_list[1])

        if len(single_rna_list) == 2:
            missing_dotbracket_and_bear_rna_molecules += '\n'.join(single_rna_list) + '\n'
        else:
            missing_bear_rna_molecules += '\n'.join(single_rna_list) + '\n'

    path_complete_input = os.path.join(dir_output, 'complete_input_with_dot_bracket_and_bear.txt')

    missing_bear_rna_molecules_all = ''
    if missing_dotbracket_and_bear_rna_molecules:
        path_missing_dot_bracket_input = os.path.join(dir_output, 'tmp.missing_dot_bracket_input.txt')
        with open(path_missing_dot_bracket_input, 'w') as fw:
            fw.write(missing_dotbracket_and_bear_rna_molecules)

        # Calculate dotbracket
        missing_bear_rna_molecules_added_dot_bracket = subprocess.check_output(
            [os.path.join(dir_base, 'scripts', 'RNAfold'), '-j 1', '--noPS', path_missing_dot_bracket_input],
            # To get strings
            universal_newlines=True
        )

        # Remove the energies
        for x in missing_bear_rna_molecules_added_dot_bracket.strip('\n>').split('\n>'):
            x_list = x.split('\n')
            x_list[2] = re.sub(r' \((.*?)\)', '', x_list[2])
            missing_bear_rna_molecules_all += '>' + '\n'.join(x_list) + '\n'

    missing_bear_rna_molecules_all += missing_bear_rna_molecules
    if missing_bear_rna_molecules_all:
        path_missing_bear_input = os.path.join(dir_output, 'tmp.missing_bear_input.txt')
        with open(path_missing_bear_input, 'w') as fw:
            fw.write(missing_bear_rna_molecules_all)

        # Calculate BEAR
        subprocess.call(
            ['java', '-jar', os.path.join(dir_base, 'scripts', 'BearEncoder_new.jar'), path_missing_bear_input,
             path_complete_input]
        )

    return path_complete_input, input_rna_to_length_dict


dir_base = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

dir_struct_motifs = os.path.join(dir_base, 'motifs_str_groups/')
dir_nucleotide_motifs = os.path.join(dir_base, 'motifs_nuc_groups/')

dir_struct_motifs_domains = os.path.join(dir_base, 'resources/dict_dom_searchMotifs_nuc.txt')
dir_nucleotide_motifs_domains = os.path.join(dir_base, 'resources/dict_dom_searchMotifs_str.txt')

search_struct_motifs = 'str'  # else ''
search_seq_motifs = 'nuc'  # else ''

species_list = sys.argv[4].split(',')
experiments_list = sys.argv[5].split(',')

user_email = sys.argv[6]

is_there_a_background = sys.argv[2]

default_search = False

# todo to activate at the end removing this line
'''
# Check if the input is the default one
DEFAULT_SEARCH_ID = 'dc4464c5cfef2f5c2fc4b08c516bfa4e'
DEFAULT_SEARCH_NUM_SEQ = 2
DEFAULT_SEARCH_SPECIES = ['hg19']
DEFAULT_SEARCH_EXPERIMENTS = ['PAR', 'eCLIP', 'HITS']

header_to_seq = {}
current_header = ''
for row in sys.argv[1].split('\n'):
    if row.startswith('>'):
        header_to_seq[row] = ''

        if len(header_to_seq) > DEFAULT_SEARCH_NUM_SEQ:
            break  # We already know this in not the default search

        current_header = row
    else:
        header_to_seq[current_header] += row

if not is_there_a_background and len(header_to_seq) == DEFAULT_SEARCH_NUM_SEQ and \
        set(species_list) == set(DEFAULT_SEARCH_SPECIES) and \
        set(experiments_list) == set(DEFAULT_SEARCH_EXPERIMENTS):

    path_complete_default_input = os.path.join(
        dir_base, 'results', DEFAULT_SEARCH_ID, 'complete_input_with_dot_bracket_and_bear.txt'
    )

    default_search = True
    with open(path_complete_default_input) as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                header = line
                seq = f.readline().strip()

                if line not in header_to_seq or header_to_seq[header] != seq:
                    default_search = False
                    break

                f.readline()  # Skip dot-bracket
                f.readline()  # Skit bear
'''
# todo to activate at the end removing this line

user_id = sys.argv[3]

dir_user = os.path.join(dir_base, 'public/results', user_id)

# Directory preparation
if not os.path.exists(dir_user):
    os.makedirs(dir_user)

if default_search:
    with open(os.path.join(dir_user, 'Out.log'), 'w') as fw:
        fw.write('dc4464c5cfef2f5c2fc4b08c516bfa4e')
        sys.exit()

path_complete_input_rna_molecules, input_rna_to_length_dict = process_input_rna_molecules(sys.argv[1], dir_user)

path_complete_input_rna_molecules_background = ''
if is_there_a_background:
    if not os.path.exists(os.path.join(dir_user, 'background')):
        os.makedirs(os.path.join(dir_user, 'background'))

    path_complete_input_rna_molecules_background, _ = process_input_rna_molecules(
        sys.argv[2], os.path.join(dir_user, 'background')
    )

path_str_or_nuc_motif_to_search_dict = {}

for str_or_nuc, dir_str_or_nuc_motifs in zip(
        [search_struct_motifs, search_seq_motifs],
        [dir_struct_motifs, dir_nucleotide_motifs],
):
    if str_or_nuc:
        path_str_or_nuc_motif_to_search_dict[str_or_nuc] = []

        for filename_motif in [x for x in os.listdir(dir_str_or_nuc_motifs) if x.startswith('motifs_')]:
            experiment, specie = filename_motif.split('_')[1:3]

            if re.findall(r"(?=(" + '|'.join(species_list) + r"))", specie) and \
                    re.findall(r"(?=(" + '|'.join(experiments_list) + r"))", experiment):
                path_str_or_nuc_motif_to_search_dict[str_or_nuc].append(
                    os.path.join(dir_str_or_nuc_motifs, filename_motif)
                )

str_or_nuc_to_input_or_background_to_output_paths_dict = {}

with open(os.path.join(dir_user, 'Out.log'), 'w') as fw:
    for str_or_nuc, dir_str_or_nuc_motifs in zip(
            [search_struct_motifs, search_seq_motifs],
            [dir_struct_motifs, dir_nucleotide_motifs],
    ):
        if str_or_nuc:
            fw.write('{} search\n'.format(str_or_nuc))
            fw.flush()

            str_or_nuc_to_input_or_background_to_output_paths_dict[str_or_nuc] = {}

            # For input and (eventually) the background
            for path_complete_input_rna_molecules_xxx, input_or_background in zip(
                    [path_complete_input_rna_molecules, path_complete_input_rna_molecules_background],
                    ['input', 'background']
            ):
                # The background path can be empty
                if path_complete_input_rna_molecules_xxx:
                    str_or_nuc_to_input_or_background_to_output_paths_dict[str_or_nuc][input_or_background] = []

                    for i, path_motif in enumerate(path_str_or_nuc_motif_to_search_dict[str_or_nuc]):
                        fw.write('search on {} database completed ({} / {}) '.format(
                            os.path.basename(path_motif), i + 1, len(path_str_or_nuc_motif_to_search_dict[str_or_nuc]))
                        )
                        fw.flush()

                        path_str_or_nuc_search_out = os.path.join(dir_user, 'search_out.{}.txt'.format(
                            os.path.basename(path_motif).split(".")[0]
                        ))
                        run_search(
                            dir_base,
                            path_motif,
                            path_complete_input_rna_molecules_xxx,
                            str_or_nuc == 'str',
                            path_str_or_nuc_search_out
                        )
                        str_or_nuc_to_input_or_background_to_output_paths_dict[str_or_nuc][
                            input_or_background
                        ].append(path_str_or_nuc_search_out)
                        fw.write('---> done\n')

input_header_to_seq_and_bear_dict = {}
with open(path_complete_input_rna_molecules) as f:
    for line in f:
        header = line.strip().lstrip('>')
        sequence = f.readline().strip()

        f.readline()  # Dot-bracket
        seq_bear = f.readline().strip()

        input_header_to_seq_and_bear_dict[header] = [sequence, seq_bear]

str_or_nuc_to_motifs_to_seq_to_info_dict = {}
str_or_nuc_to_motif_to_input_or_background_to_count_dict = {}


seq_to_str_or_nuc_to_all_motifs_dict = {}

for str_or_nuc, input_or_background_to_output_paths in str_or_nuc_to_input_or_background_to_output_paths_dict.items():
    str_or_nuc_to_motifs_to_seq_to_info_dict[str_or_nuc] = {}
    str_or_nuc_to_motif_to_input_or_background_to_count_dict[str_or_nuc] = {}

    for input_or_background, output_path_list in input_or_background_to_output_paths.items():
        for output_path in output_path_list:
            with open(output_path) as f:
                # {"chr1:149783661-149783992(-)": {"ENCFF261SMW_DDX6_UTR_m2_run1.nuc.txt": [2.7200000000000006, 11.4, 31, 12],
                seq_to_motif_to_info_dict = json.load(f)

            #               s<t s>t
            # input         x   x
            # background    x   x
            for seq, motif_to_info_dict in seq_to_motif_to_info_dict.items():
                if seq not in seq_to_str_or_nuc_to_all_motifs_dict:
                    seq_to_str_or_nuc_to_all_motifs_dict[seq] = {}
                if str_or_nuc not in seq_to_str_or_nuc_to_all_motifs_dict[seq]:
                    seq_to_str_or_nuc_to_all_motifs_dict[seq][str_or_nuc] = []

                for motif, (score, thresh, start, length) in motif_to_info_dict.items():
                    if motif not in str_or_nuc_to_motif_to_input_or_background_to_count_dict[str_or_nuc]:
                        str_or_nuc_to_motif_to_input_or_background_to_count_dict[str_or_nuc][motif] = {
                            'input': [0, 0],
                            'background': [0, 0]
                        }

                    if score < thresh:
                        str_or_nuc_to_motif_to_input_or_background_to_count_dict[str_or_nuc][motif][
                            input_or_background][0] += 1
                    else:
                        str_or_nuc_to_motif_to_input_or_background_to_count_dict[str_or_nuc][motif][
                            input_or_background][1] += 1

                        seq_to_str_or_nuc_to_all_motifs_dict[seq][str_or_nuc].append(motif)

                        if input_or_background == 'input':
                            if motif not in str_or_nuc_to_motifs_to_seq_to_info_dict[str_or_nuc]:
                                str_or_nuc_to_motifs_to_seq_to_info_dict[str_or_nuc][motif] = {}
                            str_or_nuc_to_motifs_to_seq_to_info_dict[str_or_nuc][motif][seq] = [
                                input_header_to_seq_and_bear_dict[seq][1 if str_or_nuc == 'str' else 0][start:(start + length)],
                                score,
                                len(input_header_to_seq_and_bear_dict[seq][0]),
                                start,
                                start + length - 1,
                                thresh
                            ]

if not is_there_a_background:
    with open(os.path.join(dir_base, 'resources', 'summary_AutoBg.txt')) as f:
        for line in f:
            motif, _, minor, major = line.strip().split()  # minor (s<t) and major (s>+t)

            for str_or_nuc, motif_to_input_or_background_to_count_dict in str_or_nuc_to_motif_to_input_or_background_to_count_dict.items():
                if motif in motif_to_input_or_background_to_count_dict:
                    str_or_nuc_to_motif_to_input_or_background_to_count_dict[str_or_nuc][motif]['background'] = [
                        int(minor), int(major)
                    ]


# Read domain information
motifs_to_domains_dict = {}
for str_or_nuc, dir_str_or_nuc_motifs_domains in zip(
        [search_struct_motifs, search_seq_motifs],
        [dir_struct_motifs_domains, dir_nucleotide_motifs_domains],
):
    if str_or_nuc:
        with open(dir_str_or_nuc_motifs_domains) as f:
            for line in f:
                line_split = line.strip().split('\t')

                for motif in line_split[1:]:
                    if motif not in motifs_to_domains_dict:
                        motifs_to_domains_dict[motif] = []
                    motifs_to_domains_dict[motif].append(line_split[0])

motif_results_dict = {}

for str_or_nuc, motif_to_input_or_background_to_count_dict in str_or_nuc_to_motif_to_input_or_background_to_count_dict.items():
    motif_results_dict[str_or_nuc] = {}

    for motif, input_or_background_to_count_dict in motif_to_input_or_background_to_count_dict.items():
        oddsratio, pvalue = stats.fisher_exact(
            [input_or_background_to_count_dict['input'], input_or_background_to_count_dict['background']],
            alternative='less'
        )
        motif_results_dict[str_or_nuc][motif] = [
            input_or_background_to_count_dict['input'][1] / sum(input_or_background_to_count_dict['input']),
            oddsratio, pvalue,
            motifs_to_domains_dict[motif] if motif in motifs_to_domains_dict else []
        ]


input_str_or_nuc_to_to_output_paths_dict = {}
for str_or_nuc, input_or_background_to_output_paths_dict in str_or_nuc_to_input_or_background_to_output_paths_dict.items():
    input_str_or_nuc_to_to_output_paths_dict[str_or_nuc] = input_or_background_to_output_paths_dict['input']

dir_user_download = os.path.join(dir_user, 'download')
dir_user_download_motifs = os.path.join(dir_user, 'download/motifs')
if not os.path.exists(dir_user_download_motifs):
    os.makedirs(dir_user_download_motifs)


#print(seq_to_str_or_nuc_to_all_motifs_dict)

################################################
#seq_to_str_or_nuc_to_filt_motifs_dict = {}
seq_to_sign_motifs_dict = {}

for seq, str_or_nuc_to_all_motifs_dict in seq_to_str_or_nuc_to_all_motifs_dict.items():
    #seq_to_str_or_nuc_to_filt_motifs_dict[seq] = {
    #    'str': [],
    #    'nuc': []
    #}
    seq_to_sign_motifs_dict[seq] = []

    for str_or_nuc, motif_list in str_or_nuc_to_all_motifs_dict.items():
        for motif in motif_list:
            if motif_results_dict[str_or_nuc][motif][0] > 0.5 and motif_results_dict[str_or_nuc][motif][2] < 0.05:
                #seq_to_str_or_nuc_to_filt_motifs_dict[seq][str_or_nuc].append(motif)
                seq_to_sign_motifs_dict[seq].append(motif)
################################################

for str_or_nuc, motifs_to_seq_to_info_dict in str_or_nuc_to_motifs_to_seq_to_info_dict.items():
    for motif, seq_to_info in motifs_to_seq_to_info_dict.items():
        if motif_results_dict[str_or_nuc][motif][2] < 0.05:
            with open(os.path.join(dir_user_download_motifs, motif), 'w') as fw:
                fw.write('\t'.join(['name', 'motif', 'score', 'length', 'start', 'end', 'threshold']) + '\n')

                for seq, info_list in seq_to_info.items():
                    fw.write('\t'.join([seq] + [str(x) for x in info_list]) + '\n')


species_to_protein_to_link_dict = {}

path_protein_links = os.path.join(dir_base, 'resources/protein_links.txt')
with open(path_protein_links) as f:
    f.readline()

    for line in f:
        protein_name, species, link = line.split('\t')

        if species not in species_to_protein_to_link_dict:
            species_to_protein_to_link_dict[species] = {}

        species_to_protein_to_link_dict[species][protein_name] = link.strip()


reproduciblePeakFilename_to_RBP_CellLine_dict = {}

path_eclip_cell_lines = os.path.join(dir_base, 'resources/eCLIP_CellLines.txt')
with open(path_eclip_cell_lines) as f:
    f.readline()

    for line in f:
        RBP, CellLine, ReproduciblePeakFilename = line.strip().split('\t')

        if ReproduciblePeakFilename not in reproduciblePeakFilename_to_RBP_CellLine_dict:
            reproduciblePeakFilename_to_RBP_CellLine_dict[ReproduciblePeakFilename] = {}

        reproduciblePeakFilename_to_RBP_CellLine_dict[ReproduciblePeakFilename] = [RBP, CellLine]


publication_to_Link_dict = {}

path_eclip_cell_lines = os.path.join(dir_base, 'resources/publications_CLIP_data.txt')
with open(path_eclip_cell_lines) as f:
    f.readline()

    for line in f:
        publication, link = line.strip().split('\t')

        if publication not in publication_to_Link_dict:
            publication_to_Link_dict[publication] = {}

        publication_to_Link_dict[publication] = link



os.system("cp " + os.path.join(dir_base, 'public/examples/README.txt') + " " + dir_user_download)

output_generation.generate_output(
    dir_base,
    path_complete_input_rna_molecules,
    os.path.join(dir_user, 'results.html'),
    os.path.join(dir_user_download, 'tab_sequences.txt'),
    os.path.join(dir_user_download, 'tab_enriched_motifs.txt'),
    dir_user_download,
    input_str_or_nuc_to_to_output_paths_dict,
    motif_results_dict,
    seq_to_sign_motifs_dict,
    user_email,
    species_to_protein_to_link_dict,
    reproduciblePeakFilename_to_RBP_CellLine_dict,
    publication_to_Link_dict
)

with open(os.path.join(dir_user, 'Out.log'), 'w') as fw:
    fw.write('100')

# Remove temporary files
for path_tmp_file in [os.path.join(dir_user, x) for x in os.listdir(dir_user) if x.startswith('tmp.')]:
    print('Remove', path_tmp_file)
    os.remove(path_tmp_file)
