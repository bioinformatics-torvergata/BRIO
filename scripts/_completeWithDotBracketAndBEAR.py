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

def run_search(dir_base, path_motif, path_input_seq_struct_bear, str_else_nuc):
    if str_else_nuc:
        return subprocess.check_output(
            [
                'java', '-jar', os.path.join(dir_base, 'scripts', 'search1.2.jar'),
                path_motif,
                path_input_seq_struct_bear
            ],
            # To get strings
            universal_newlines=True
        )
    else:
        return subprocess.check_output(
            [
                'python3', os.path.join(dir_base, 'scripts', 'Search_nt.py'),
                path_motif,
                path_input_seq_struct_bear,
            ],
            # To get strings
            universal_newlines=True
        )

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

dir_struct_motifs = os.path.join(dir_base, 'some_motifs_str/')
dir_nucleotide_motifs = os.path.join(dir_base, 'some_motifs_nuc/')

is_there_a_background = sys.argv[2]

# To get from user input?
search_struct_motifs = 'str' #else ''
search_seq_motifs = 'nuc' #else ''

dir_user = os.path.join(dir_base, 'results',
    ''.join(choice(ascii_uppercase) for i in range(32))
)


# Directory preparation
if not os.path.exists(dir_user):
    os.makedirs(dir_user)

path_complete_input_rna_molecules, input_rna_to_length_dict = process_input_rna_molecules(sys.argv[1], dir_user)

path_complete_input_rna_molecules_background = ''
if is_there_a_background:
    if not os.path.exists(os.path.join(dir_user, 'background')):
        os.makedirs(os.path.join(dir_user, 'background'))

    path_complete_input_rna_molecules_background, _ = process_input_rna_molecules(sys.argv[2], os.path.join(dir_user, 'background'))


# To load this one-time only when the server starts and for all the users(?)
protein_to_domains_dict = {}
with open(os.path.join(dir_base, 'resources', 'dict_prot_dom.txt')) as f:
    for line in f:
        line_list = line.strip('\n').split('\t')
        protein_to_domains_dict[line_list[0].upper()] = line_list[1:]
        
# To load this one-time only when the server starts and for all the users(?)
str_or_nuc_motif_to_threshold_dict = {
    'str': {},
    'nuc': {}
}
for str_or_nuc in str_or_nuc_motif_to_threshold_dict.keys():
    with open(os.path.join(dir_base, 'resources', 'dict_{}.txt'.format(str_or_nuc))) as f:
        for line in f:
            key, value = line.strip('\n').split('\t')
            str_or_nuc_motif_to_threshold_dict[str_or_nuc][key] = float(value)


if not is_there_a_background:
    #creo dizionario per bg: chiave=nome, lista=[major, minor]
    f=open(os.path.join(dir_base, 'resources', 'summary_AutoBg.txt'))
    line=f.readline()
    dict_bg={}
    while (line):
        dict_bg[line.split()[0]]=[int(line.split()[2]),int(line.split()[3])]
        line=f.readline()
    f.close()

for str_or_nuc, dir_str_or_nuc_motifs in zip(
    [search_struct_motifs, search_seq_motifs],
    [dir_struct_motifs, dir_nucleotide_motifs]
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
                input_or_background_to_result_to_output_dict[input_or_background] = {}

                for filename_motif in os.listdir(dir_str_or_nuc_motifs):
                    input_or_background_to_result_to_output_dict[input_or_background][filename_motif] = run_search(
                        dir_base,
                        os.path.join(dir_str_or_nuc_motifs, filename_motif),
                        path_complete_input_rna_molecules_xxx,
                        str_or_nuc == 'str',
                    )

        result_to_write_list = []
        for motif_key, output_result in input_or_background_to_result_to_output_dict['input'].items():
            perc, major, minor = perc_seq_motif(
                motif_key,
                output_result,
                str_or_nuc_motif_to_threshold_dict[str_or_nuc],
                str_or_nuc == 'str'
            )

            if 'background' in input_or_background_to_result_to_output_dict.keys(): #is_there_a_background:
                perc_bg, major_bg, minor_bg = perc_seq_motif(
                    motif_key,
                    input_or_background_to_result_to_output_dict['background'][motif_key],
                    str_or_nuc_motif_to_threshold_dict[str_or_nuc],
                    str_or_nuc == 'str'
                )
            else:
                major_bg=dict_bg[motif_key][0]
                minor_bg=dict_bg[motif_key][1]

            #calcolo fisher test
            oddsratio, pvalue = stats.fisher_exact([[major, major_bg], [minor, minor_bg]])

            motif_name = Search_motif_name(os.path.join(dir_str_or_nuc_motifs, motif_key))
            regione = str(motif_key.split('_')[-3])
            n_motif = str(motif_key.split('_')[-2])
            RBP_name = str(motif_key.split('_')[1])
            #scrivo modello, regione, numero motivo, perc|oddsratio|p-value, nome del file con i risultati (che potra' essere scaricato), nome rbp
            row_to_write = motif_name+"\t"+regione+"\t"+n_motif+"\t"+str(round(perc,2))+"|"+str(round(oddsratio,2))+"|"+str(pvalue)+"\t"+motif_key+"\t"+RBP_name

            # Add domains
            if RBP_name.upper() in protein_to_domains_dict.keys():
                row_to_write += '\t' + '\t'.join(
                    [protein_to_domains_dict[RBP_name.upper()][-1]] + protein_to_domains_dict[RBP_name.upper()][:-1]
                )

            result_to_write_list.append(row_to_write)

        path_str_or_nuc_search_out = os.path.join(dir_user, 'search_out.{}.txt'.format(str_or_nuc))
        with open(path_str_or_nuc_search_out, 'w') as f:
            f.write('\n'.join(result_to_write_list) + '\n')

        # =================================================================
        # Make summary: TO DO ONLY IF THE USER DOWNLOAD THE RESULTS?
        # ============
        dir_summary_str_or_nuc = os.path.join(dir_user, 'summary_{}'.format(str_or_nuc))
        if not os.path.exists(dir_summary_str_or_nuc):
            os.makedirs(dir_summary_str_or_nuc)
        for motif_key, output_result in input_or_background_to_result_to_output_dict['input'].items():
            result_summary_to_write_list = []
            threshold = str_or_nuc_motif_to_threshold_dict[str_or_nuc][motif_key]

            if str_or_nuc == 'str':
                file_list = output_result.strip('\n').split('\n')[5:-5]
                for i in range(0, len(file_list) - 1, 2):
                    tmp_list = ['', '', '', '', '', '', '']

                    splitted_list = file_list[i+1].strip('[INFO]\n').split('\t')

                    tmp_list[0] = file_list[i].strip('[INFO]\n')
                    tmp_list[1] = splitted_list[0]
                    tmp_list[2] = splitted_list[3]
                    tmp_list[3] = str(input_rna_to_length_dict[tmp_list[0]])
                    tmp_list[4] = splitted_list[1]
                    tmp_list[5] = splitted_list[2]
                    tmp_list[6] = str(threshold)
                    result_summary_to_write_list.append(tmp_list)
            else:
                for line in output_result.strip('\n').split('\n'):
                    result_summary_to_write_list.append(
                        line.strip('\n').split('\t') + [str(threshold)]
                    )

            with open(os.path.join(
                    dir_summary_str_or_nuc,
                    motif_key + '.summary.txt'
                ), 'w') as f:
                f.write('name\tmotif\tscore\tlength\tstart\tend\tthreshold\n')
                f.write('\n'.join(
                    ['\t'.join(x_list) for x_list in sorted(result_summary_to_write_list, key=lambda x: x[2], reverse=True)]
                ) + '\n')
            # =================================================================


        '''
        # MAYBE TO DELETE
        # =============================================
        # # Domains search
        # =================
        # To load this one-time only when the server starts and for all the users(?)
        make_search_str_or_nuc_list = []
        with open(os.path.join(dir_base, 'resources', 'dict_dom_searchMotifs_{}.txt'.format(str_or_nuc))) as f:
            for line in f:
                make_search_str_or_nuc_list += line.strip('\n').split('\t')[1:]

        str_or_nuc_motifs_to_search_set = set(os.listdir(dir_str_or_nuc_motifs)).intersection(set(make_search_str_or_nuc_list))

        dir_user_output_base = os.path.join(dir_user, 'out_search_{}'.format(str_or_nuc))
        for single_search_str_or_nuc in sorted(str_or_nuc_motifs_to_search_set):
            #file_out=folder+'out_search_str/'+motif.split('.')[0]+'_out_search.str.txt'
            path_str_or_nuc_output = os.path.join(dir_user_output_base, single_search_str_or_nuc.split('.')[0] + '_out_search.{}.txt'.format(str_or_nuc))

            file_name_logo=single_search_str_or_nuc.split('.txt')[0]
            print(path_str_or_nuc_output)
            #os.system('cp /home/sangiovanni/public_html/brio/motifs_logo/str/'+file_name_logo+'* '+folder+'/logos/')
            #run_search('motifs_str/', motif, file_bear,file_out,'str',folder)
        '''


print('END')

# To remove temporary files (path_missing_dot_bracket_input, path_missing_bear_input, ...)
