import json

def generate_output(path_results_html, path_processed_input, sequence_results_dict, motif_results_dict):
    """
    path_results_html is the path of the output page to create

    path_processed_input is the path of the input file plus dot bracket and BEAR strings
        >seq1
        AGCA...
        .(((...
        :GGG...
        >seq2
        ...

    sequence_results_dict contains the paths of the resulting files, divided by sequences (seq) and structure (str)
    {
        'str': ['~/BRIO/results/<random_code>/search_out.motifs_PAR_hg19_str.txt', ...],
        'nuc': ['~/BRIO/results/<random_code>/search_out.motifs_PAR_hg19_seq.txt', ...]
    }

    motif_results_dict contains the enrichment information for each motif (motif_name: [coverage, odds ratio, p-value)
    {
        'HITSCLIP_Nova_Zhang2011b_mm9_CDS_m1_run2.txt': [52.63, 9.78, 8.38e-05],
         ...
    }

    :return: nothing
    """

    # Dirty temporary solution
    # "best_score\tmotif_threshold\tposition\tmotif_size"
    with open(path_results_html, 'w') as fw:
        for str_or_nuc, path_str_or_nuc_search_out_list in sequence_results_dict.items():
            fw.write('<h3>{}</h3>'.format(str_or_nuc))
            for path_str_or_nuc_search_out in path_str_or_nuc_search_out_list:
                fw.write('<h5>{}</h5>'.format(path_str_or_nuc_search_out.split('/')[-1]))

                with open(path_str_or_nuc_search_out) as f:
                    # {">chr1:149783661-149783992(-)": {"ENCFF261SMW_DDX6_UTR_m2_run1.nuc.txt": [2.7200000000000006, 11.4, 31, 12],
                    seq_to_motif_to_info_dict = json.load(f)


                for k, v in seq_to_motif_to_info_dict.items():
                    fw.write("{}".format(k))
                    fw.write('''<table>
                      <tr>
                        <th>Motif</th>
                        <th>InfoMatch</th>
                        <th>Statistics</th>
                      </tr>
                      '''
                    )
                    for motif, vv in v.items():
                        if vv[0] >= vv[1] and motif_results_dict[motif][2] <= 0.05:
                            fw.write("<tr>")
                            fw.write('<td>{}</td><td>{}</td><td>{}</td>'.format(motif, vv, motif_results_dict[motif]))
                            fw.write("</tr>")
                    fw.write('</table>')
            fw.write("<hr/>")
