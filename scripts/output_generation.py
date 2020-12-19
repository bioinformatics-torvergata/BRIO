import json
import os
import my_email

def generate_output(dir_base, path_results_html, dir_user_download, sequence_results_dict, motif_results_dict, user_email):
    """
    dir_base is the base directory of BRIO on the server

    path_results_html is the path of the output page to create

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

    :return: nothing
    """

    # Dirty temporary solution
    # "best_score\tmotif_threshold\tposition\tmotif_size"
    user = dir_user_download.split("/")[-2]
    os.system("mkdir " + dir_user_download + "/logos")

    with open(path_results_html, 'w') as fw:

        fw.write('<br>Click here to download all your results \n')
        fw.write(
            '<a href="results/' + user + '/download.zip" download><button class="btn"><i class="fa fa-download"></i> Download</button></a>\n<br>\n')

        fw.write(
            '<script>\n$(document).ready(function()\n{\n$("#sequence").tablesorter({\nsortList: [[4,0]],\nheaders: {0:{sorter:false},8:{sorter:false}}\n});\n}\n);\n</script>')
        fw.write(
            '\n<script>\n$(document).ready(function()\n{\n$("#structure").tablesorter({\nsortList: [[4,0]],\nheaders: {0:{sorter:false},8:{sorter:false}}\n});\n}\n);\n</script>')

        fw.write('<div class="tab">\n<button class="tablinks" onclick="openCity(event, \'London\')" id="defaultOpen">Structure</button>\n')
        fw.write('<button class="tablinks" onclick="openCity(event, \'Paris\')">Sequence</button>\n')
        fw.write('</div>')

        for str_or_nuc in sequence_results_dict:
            if str_or_nuc == "str":
                fw.write('<div id="London" class="tabcontent">\n<table id="structure"')
            else:
                fw.write('<div id="Paris" class="tabcontent">\n<table id="sequence"')
            fw.write(
                ' class="out_table">\n<thead>\n<tr>\n<th>Motif</th>\n<th>Region </th>\n<th>Coverage </th>\n<th> oddsratio </th>\n<th> p-value </th>\n<th>Protein </th>\n<th>Domains </th>\n<th>Organism </th>\n<th>Download</th></tr>\n</thead>\n<tbody>\n')

            for motif in motif_results_dict[str_or_nuc]:

                if str_or_nuc == "nuc":
                    path_logo_on_server = os.path.join(dir_base, 'public/images/logos', motif.split(".")[0] + "_wl.nuc.png")
                    logo_link = "../images/logos/" + motif.split(".")[0] + "_wl.nuc.png"
                else:
                    path_logo_on_server = os.path.join(dir_base, 'public/images/logos', motif.split(".")[0] + "_wl.png")
                    logo_link = "../images/logos/" + motif.split(".")[0] + "_wl.png"

                os.system("cp " + path_logo_on_server + " " + dir_user_download + "/logos/")

                coverage = str("%.2g" % motif_results_dict[str_or_nuc][motif][0])
                oddsratio = str("%.2g" % motif_results_dict[str_or_nuc][motif][1])
                p_value = str("%.2g" % motif_results_dict[str_or_nuc][motif][2])
                region = motif.split("_")[-3]
                protein = motif.split("_")[1]
                if motif_results_dict[str_or_nuc][motif][3]:
                    domains = "\n".join(motif_results_dict[str_or_nuc][motif][3])
                else:
                    domains = " - "
                if "_mm9_" in motif:
                    organism = "Mus musculus"
                else:
                    organism = "Homo sapiens"

                if float(p_value) >= 0.05:
                    continue
                if float(coverage) <= 0.5:
                    continue

                fw.write(
                    '<td> <div style="width:250px;height:100px"><img src="' + logo_link + '" width="100%" height="100%" ></div></td>\n')
                fw.write('<td><div >' + region + '</div></td>\n')
                fw.write('<td><div > ' + coverage + '</div></td>\n')
                fw.write('<td><div > ' + oddsratio + ' </div></td>\n')
                fw.write('<td><div > ' + p_value + ' </div></td>\n')
                fw.write('<td><div > ' + protein + ' </div></td>\n')
                fw.write('<td><div > ' + domains + ' </div></td>\n')
                fw.write('<td><div > ' + organism + ' </div></td>\n')
                # fw.write('<td><div > prova </div></td>\n</tr>\n')
                fw.write(
                    '<td><div ><a href="results/' + user + '/download/' + motif + '" Download><button class="btn"><i class="fa fa-download"></i>Download</button></a></div></td>\n</tr>\n')
                # <button class="btn"><i class="fa fa-download"></i> Show file</button></a></div></td>\n</tr>\n')

            fw.write("</tbody>\n</table>\n</div>\n")

        fw.write('\n<script>\nfunction openCity(evt, cityName) {\n')
        fw.write('var i, tabcontent, tablinks;\ntabcontent = document.getElementsByClassName("tabcontent");\n')
        fw.write('for (i = 0; i < tabcontent.length; i++) {\ntabcontent[i].style.display = "none";\n}\n')
        fw.write('tablinks = document.getElementsByClassName("tablinks");\n')
        fw.write('for (i = 0; i < tablinks.length; i++) {\n')
        fw.write('tablinks[i].className = tablinks[i].className.replace(" active", "");\n}\n')
        fw.write('document.getElementById(cityName).style.display = "block";\n')
        fw.write('evt.currentTarget.className += " active";\n}\n')
        fw.write('document.getElementById("defaultOpen").click();\n</script>\n')

    os.system(
        "zip -j " + os.path.join(os.path.dirname(dir_user_download), "download") + " " +
        os.path.join(dir_user_download, "*.txt") + " " +
        os.path.join(dir_user_download, "logos/*.png") + " " +
        path_results_html
    )

    if user_email != '':
        my_email.send_email_with_code(code=user, user_email=user_email)