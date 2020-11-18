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
                    fw.write('{}<br/>'.format(f.read()))

            fw.write("<hr/>")
