import json
import os
import my_email
import shutil


def generate_output(dir_base, path_complete_input_rna_molecules,
                    path_results_html, path_tab_sequences_txt, path_tab_enriched_motifs_txt,
                    dir_user_download,
                    sequence_results_dict, motif_results_dict, seq_to_sign_motifs_dict,
                    user_email, species_to_protein_to_link_dict,
                    reproduciblePeakFilename_to_RBP_CellLine_dict, publication_to_Link_dict):
    """
    dir_base is the base directory of BRIO on the server

    path_complete_input_rna_molecules complete valid user input
    >header
    sequence
    dot-bracket
    brear
    >header
    ...

    path_results_html is the path of the output page to create

    path_tab_sequences_txt is the path of the txt file to create for the tab sequences

    path_tab_enriched_motifs_txt is the path of the txt file to create for the tab enriched motifs

    dir_user_download: subfolder which contains a file for each motif, with information regarding the matches in each input sequence

    sequence_results_dict contains the paths of the resulting files, divided by sequences (seq) and structure (str)
    {
        'str': ['~/BRIO/results/<random_code>/search_out.motifs_PAR_hg19_str.txt', ...],
        'nuc': ['~/BRIO/results/<random_code>/search_out.motifs_PAR_hg19_seq.txt', ...]
    }

    motif_results_dict contains the enrichment information for each motif (motif_name: [coverage, odds ratio, p-value)
    {
        'str': 'HITSCLIP_Nova_Zhang2011b_mm9_CDS_m1_run2.txt': [52.63, 9.78, 8.38e-05, [domain1, domain2, ...],
        'nuc': ...
    }

    seq_to_sign_motifs_dict
    {
        'header' : ['HITSCLIP_Nova_Zhang2011b_mm9_CDS_m1_run2.txt', ...], ...
    }

    user_email

    species_to_protein_to_link_dict:
    {
        'hg19': {
            Nova_: link to the UniprotId page of the protein,
            }
    }

    ReproduciblePeakFilename_to_RBP_CellLine_dict:
    {
        'ENCFF105AKX' : ['HNRNPC', 'HepG2'], ...
    }

    publication_to_Link_dict:
    {
        'Kishore2011a' : 'https://www.nature.com/articles/nmeth.1608?page=14', ...
    }

    :return: nothing
    """

    # Dirty temporary solution
    # "best_score\tmotif_threshold\tposition\tmotif_size"

    table_empty = True
    for str_or_nuc in sequence_results_dict:
        for motif in motif_results_dict[str_or_nuc]:
            p_value = str("%.2g" % motif_results_dict[str_or_nuc][motif][2])
            if float(p_value) >= 0.05:
                continue

            coverage = str("%.2g" % motif_results_dict[str_or_nuc][motif][0])
            if float(coverage) <= 0.5:
                continue

            table_empty = False
            break

        if not table_empty:
            break

    user = dir_user_download.split("/")[-2]
    os.system("mkdir " + dir_user_download + "/logos")

    total_file_dict = {}
    files = os.listdir(dir_user_download + "/motifs/")
    for file in files:
        opened_file = open(dir_user_download + "/motifs/" + file).readlines()
        for line in opened_file[1:]:
            split_line = line.split("\t")
            if file not in total_file_dict:
                total_file_dict[file] = {}

            total_file_dict[file][split_line[0]] = split_line[1:]

    with open(path_results_html, 'w') as fw:
        fw.write("<br>Click here to download your input\n")
        fw.write(
            '<a href="results/' + user + '/complete_input_with_dot_bracket_and_bear.txt" download><button class="btn"><i class="fa fa-download"></i> Download</button></a>\n<br>')

        if not table_empty:
            fw.write('Click here to download all your results \n')
            fw.write(
                '<a href="results/' + user + '/download.zip" download><button class="btn"><i class="fa fa-download"></i> Download</button></a>\n<br>\n')

            # fw.write(
            #    '<script>\n$(document).ready(function()\n{\n$("#sequence").tablesorter({\nsortList: [[4,0]],\nheaders: {0:{sorter:false},8:{sorter:false}}\n});\n}\n);\n</script>')
            fw.write(
                '\n<script>\n$(document).ready(function()\n{\n$("#structure").tablesorter({\nsortList: [[4,0]],\nheaders: {0:{sorter:false},11:{sorter:false}}\n});\n}\n);\n</script>')

            count = 1
            for single in seq_to_sign_motifs_dict:
                fw.write('\n<script>\n$(document).ready(function()\n{\n$("#group-of-rows-' + str(
                    count) + '").tablesorter({\nsortList: [[0,0]],\nheaders: {2:{sorter:false}}\n});\n}\n);\n</script>')
                count += 1

            fw.write(
                '<div class="tab">\n<button class="tablinks" onclick="openCity(event, \'London\')" id="defaultOpen">Enriched Motifs</button>\n')
            fw.write('<button class="tablinks" onclick="openCity(event, \'Paris\')" >Sequences</button>\n')
            fw.write('</div>')

            # if str_or_nuc == "str":
            fw.write('<div id="London" class="tabcontent">\n<table id="structure"')
            # else:
            #    fw.write('<div id="Paris" class="tabcontent">\n<table id="sequence"')
            fw.write(' class="out_table">\n<thead>\n<tr>\n')
            fw.write(
                '<th title="The logo of the secondary structure motif in the BEAR alphabet or, in case of sequence motifs, in the IUPAC nucleic acid notation (logos have been generated using WebLogo (Crooks et al., 2004)">Logo</th>\n')
            fw.write('<th title="The type of motif: structural or sequence motif">Type</th>\n')
            fw.write(
                '<th title="The type of mapping regions from gencode annotation of the RNAs datasets where the motif was originally found">Region </th>\n')
            fw.write(
                '<th title="The number of input sequences in which the motif has a score higher than its associated threshold, divided by the number of query sequences">Coverage </th>\n')
            fw.write('<th title="The Fisher’s Test p-value"> p-value </th>\n')
            fw.write('<th title="The type of the CLIP experiment analyzed">Experiment </th>\n')
            fw.write(
                '<th title="The protein associated to the RNA secondary structure motif in the CLIP experiment analyzed">Protein </th>\n')
            fw.write(
                '<th title="The protein domain associated to the RNA secondary structure motif (this information is not always available)">Domains </th>\n')
            fw.write(
                '<th title="Cell line used in this experiment (available only for eCLIP)">Cell line </th>\n')
            fw.write(
                '<th title="Experiment information:\n Reproducible Peak Filename (eCLIP)\n Article link (PAR-CLIP,HIT-CLIP)">Experiment Info </th>\n')
            fw.write(
                '<th title="The organism in which the experiment was performed">Organism </th>\n<th>Download</th></tr>\n</thead>\n<tbody>\n')

            for str_or_nuc in sequence_results_dict:
                if str_or_nuc == "str":
                    tipo = "Structure"
                else:
                    tipo = "Sequence"
                for motif in motif_results_dict[str_or_nuc]:
                    p_value = str("%.2g" % motif_results_dict[str_or_nuc][motif][2])
                    if float(p_value) >= 0.05:
                        continue

                    if str_or_nuc == "nuc":
                        path_logo_on_server = os.path.join(dir_base, 'public/images/logos', motif.split(".")[0] + "_wl.nuc.png")
                        logo_link = "../images/logos/" + motif.split(".")[0] + "_wl.nuc.png"
                    else:
                        path_logo_on_server = os.path.join(dir_base, 'public/images/logos', motif.split(".")[0] + "_wl.png")
                        logo_link = "../images/logos/" + motif.split(".")[0] + "_wl.png"

                    os.system("cp " + path_logo_on_server + " " + dir_user_download + "/logos/")

                    coverage = str("%.2g" % motif_results_dict[str_or_nuc][motif][0])
                    if float(coverage) <= 0.5:
                        continue

                    oddsratio = str("%.2g" % motif_results_dict[str_or_nuc][motif][1])

                    region = motif.split("_")[-3]
                    protein = motif.split("_")[1]

                    if motif.startswith("ENC"):
                        experiment = "eCLIP"
                    else:
                        experiment = motif.split("_")[0]

                    if motif_results_dict[str_or_nuc][motif][3]:
                        domains = ";<br/>".join(motif_results_dict[str_or_nuc][motif][3]) + ';'
                    else:
                        domains = " - "
                    if "_mm9_" in motif:
                        organism = "Mus musculus"
                    else:
                        organism = "Homo sapiens"

                    fw.write(
                        '<td> <div style="width:250px;height:100px"><img src="' + logo_link + '" width="100%" height="100%" ></div></td>\n')
                    fw.write('<td><div>' + tipo + '</div></td>\n')
                    fw.write('<td><div>' + region + '</div></td>\n')
                    fw.write('<td><div> ' + coverage + '</div></td>\n')
                    fw.write('<td><div> ' + p_value + ' </div></td>\n')
                    fw.write('<td><div> ' + experiment + ' </div></td>\n')

                    if "_mm9_" in motif:
                        species = "mm9"
                    else:
                        species = "hg19"

                    if protein in species_to_protein_to_link_dict[species] and species_to_protein_to_link_dict[species][
                        protein]:
                        fw.write(
                            f'<td><div><a href="{species_to_protein_to_link_dict[species][protein]}" target="_blank">' + protein + ' </div></td>\n')
                    else:
                        fw.write('<td><div> ' + protein + ' </div></td>\n')
                    
                    fw.write('<td><div> ' + domains + ' </div></td>\n')

                    cell_lines=" - "
                    info=" - "
                    if experiment=="eCLIP":
                    	if motif.split("_")[0] in reproduciblePeakFilename_to_RBP_CellLine_dict:
                    		cell_lines=reproduciblePeakFilename_to_RBP_CellLine_dict[motif.split("_")[0]][1]
                    		info=motif.split("_")[0]
                    else:
                    	if motif.split("_")[2] in publication_to_Link_dict:
                    		info=publication_to_Link_dict[motif.split("_")[2]]
                    
                    fw.write('<td><div> ' + cell_lines + ' </div></td>\n')
                    
                    if experiment=="eCLIP":
                    	fw.write('<td><div> ' + info + ' </div></td>\n')
                    else:
	                    fw.write('<td><div> <a href="' + info + '" target="_blank"> Article link </div></td>\n')

                    fw.write('<td><div><i>' + organism + ' </i></div></td>\n')
                    # fw.write('<td><div > prova </div></td>\n</tr>\n')
                    fw.write(
                        '<td><div ><a href="results/' + user + '/download/motifs/' + motif + '" Download><button class="btn"><i class="fa fa-download"></i>Download</button></a></div></td>\n</tr>\n')
                    # <button class="btn"><i class="fa fa-download"></i> Show file</button></a></div></td>\n</tr>\n')

            fw.write("</tbody>\n</table>\n</div>\n")

            fw.write(
                '<div id="Paris" class="tabcontent">\n<table id="sequence" class="table table-responsive table-hover out_table">\n')
            fw.write(
                '<thead>\n<tr>\n<th></th>\n<th title="The name of the input sequence"><div style="width:250px">Name</div></th>\n<th title="The number of the identified sequence motifs"><div style="width:170px"># Sequence motifs</div></th>\n<th title="The number of the identified structural motifs"><div style="width:170px"># Structure motifs </div></th>\n<th title="The input sequence length"> <div style="width:170px"> Length </div></th>\n</tr>\n</thead>\n<tbody>\n')
            count = 1
            for single_input in seq_to_sign_motifs_dict:
                if count != 1:
                    fw.write('<table id="sequence" class="table table-responsive table-hover out_table">\n')
                fw.write('<tr class="clickable" data-toggle="collapse" data-target="#group-of-rows-' + str(
                    count) + '" aria-expanded="false" aria-controls="group-of-rows-' + str(count) + '">')
                fw.write('<td><i class="fa fa-plus" aria-hidden="true"></i></td>')
                seq_number = sum(['nuc' in x for x in seq_to_sign_motifs_dict[single_input]])
                str_number = len(seq_to_sign_motifs_dict[single_input]) - seq_number
                for k in total_file_dict:
                    if single_input in total_file_dict[k]:
                        length = str(total_file_dict[k][single_input][2])

                fw.write('<td><div style="width:250px">' + single_input + '</div></td>\n')
                fw.write('<td><div style="width:170px">' + str(seq_number) + '</div></td>\n')
                fw.write('<td><div style="width:170px">' + str(str_number) + '</div></td>\n')
                fw.write('<td><div style="width:170px">' + length + ' </div></td></tr>\n')

                fw.write('<table id="group-of-rows-' + str(count) + '" class="collapse">\n')
                fw.write(
                    '<thead>\n<tr>\n<th title="The start position of the motif">Start</th>\n<th title="The end position of the motif">End</th>\n<th title="The representation of the motif in BEAR alphabet for structure motifs or in IUPAC nucleic acid notation for sequence motifs">Motif</th>\n<th title="The tipe of motif:sequence or structural">Type</th>\n<th title="The protein associated with the RNA secondary structure motif in the CLIP experiment">Protein</th>\n<th title="The tipe of CLIP experiment">Experiment</th>\n</thead>\n<tbody>\n')
                for m in seq_to_sign_motifs_dict[single_input]:
                    if 'nuc' in m:
                        motif_type = "Sequence"
                    else:
                        motif_type = "Structure"
                    if m.startswith("ENC"):
                        experiment = "eCLIP"
                    else:
                        experiment = m.split("_")[0]
                    protein = m.split("_")[1]

                    motif_string = total_file_dict[m][single_input][0]
                    start = str(total_file_dict[m][single_input][3])
                    end = str(total_file_dict[m][single_input][4])
                    fw.write(
                        '<td>' + start + '</td>\n<td>' + end + '</td>\n<td>' + motif_string + '</td>\n<td>' + motif_type + '</td>\n')
                    if protein in species_to_protein_to_link_dict[species] and species_to_protein_to_link_dict[species][
                        protein]:
                        fw.write(
                            f'<td><div><a href="{species_to_protein_to_link_dict[species][protein]}" target="_blank">' + protein + ' </div></td>\n')
                    else:
                        fw.write('<td><div> ' + protein + ' </div></td>\n')
                    fw.write('<td>' + experiment + '</td>\n</tr>\n')

                fw.write('</table></tbody>')
                count += 1

            fw.write('</tbody>\n')
            fw.write('</table>\n')

            fw.write('</div></div></div>')

            fw.write('\n<script>\nfunction openCity(evt, cityName) {\n')
            fw.write('var i, tabcontent, tablinks;\ntabcontent = document.getElementsByClassName("tabcontent");\n')
            fw.write('for (i = 0; i < tabcontent.length; i++) {\ntabcontent[i].style.display = "none";\n}\n')
            fw.write('tablinks = document.getElementsByClassName("tablinks");\n')
            fw.write('for (i = 0; i < tablinks.length; i++) {\n')
            fw.write('tablinks[i].className = tablinks[i].className.replace(" active", "");\n}\n')
            fw.write('document.getElementById(cityName).style.display = "block";\n')
            fw.write('evt.currentTarget.className += " active";\n}\n')
            fw.write('document.getElementById("defaultOpen").click();\n</script>\n')

            shutil.make_archive(os.path.join(os.path.dirname(dir_user_download), "download"), 'zip', dir_user_download)
        else:
            fw.write('<h2 class="text-center"">Sorry, no results found.</h2>')

    shutil.copyfile(path_complete_input_rna_molecules, os.path.join(dir_user_download, 'input.txt'))

    if user_email != '':
        my_email.send_email_with_code(code=user, user_email=user_email)
