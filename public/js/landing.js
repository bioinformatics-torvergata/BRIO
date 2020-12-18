$(function () {

    //format popovers
    //$('[data-toggle="popover"]').popover();

    $('#format_pop_1').popover({
        html: true,
        content: 'input sequences are accepted in multiFASTA format\
        and are parsed as blocks. For each sequence:\
  			<ul><li>The line containing the name and/or the description of the \
  			sequence starts with a ">";</li><li> \
			The words following the ">" are interpreted as the RNA id;</li><li>\
			The subsequent line(s) should be the RNA nucleotide sequence. \
      Multiline FASTA are accepted;</li><li>\
			The subsequent block can contain secondary structure information (Optional\
			in dot-bracket);</li></ul>\
			<em>(click again to dismiss)</em>',
        placement: 'right'
    });

    $(".chosen-select").chosen({
        no_results_text: "Oops, nothing found!"
    });

    //populate text area with examples
    $("#ex_w_str").click(function () {
        $("#inputRNA").val(
            ">chr1:149783661-149783992(-)\n" +
            "AGCACUUUGCGAGUCUUCAUUUGCAUACGGGCUCUAUAAGUAGCGCAUAACCAGCCCGUUUUGCGGUAGUUCGGAUUACUUCUUUAAGUCUCUUUUCUCUUUUUUCGCGCAAAAAUGCCGGAUCCAGCGAAAUCCGCUCCUGCUCCCAAGAAGGGCUCCAAAAAGGCUGUUACGAAAGUGCAGAAGAAGGACGGCAAGAAGCGCAAGCGCAGCCGCAAGGAGAGCUACUCCGUUUACGUGUACAAGGUGCUGAAGCAGGUCCACCCCGACACCGGCAUCUCGUCCAAGGCCAUGGGCAUCAUGAACUCCUUCGUCAACGACAUCUUCGAGC\n" +
            ".(((((((..((((((............)))))).....(((((((......(((((.(((((.(((((..((((((((((....))))......((.((...((((.(((....)))))))...)).))))))))...)))))..))))).)))))........)).))))).))))))).((.((((((((((.....((....))...))))...((((.....)))).............((((((((..(..((......))..)..)))))))).(((((......))))).........)))))).))..(((.....)))...\n" +
            ">chr1:149784741-149784985(-)\n" +
            "CUUCCAGAGCUCGGCCGUGAUGGCGCUGCAGGAGGCCAGCGAGGCCUACCUGGUGGGGCUGUUCGAAGACACGAACCUGUGCGCCAUCCAUGCCAAGCGCGUGACCAUCAUGCCCAAGGACAUCCAGUUGGCCCGCCGCAUCCGCGGGGAGCGGGCCUAAGGCAUAUUUUUAAGUGGUCGAUCUAAAGGCUCUUUUCAGAGCCACUGCCGUUUUCAUCAAGAGCAGCUGUACCGGCUCUCCAUC\n" +
            ".....(((((.(((..(.((((((((.(((((((.((.((.(((....))).)).)).)).((((......))))))))))))))))))((((.....))))((((((.(((((...((....))....(((((((....(((....))))))))))...)))))........))))))........((((((....))))))((.((.(((((.....))))).)).)).)))))))).....\n"
        );
        /*$.ajax({
            url: "examples/example_w_struct.txt",
            dataType: "text",
            success: function (data) {
                $("#inputRNA").val(data);
            }
        });*/
    });
    $("#ex_wo_str").click(function () {
        $("#inputRNA").val(
            ">chr1:149783661-149783992(-)\n" +
            "AGCACUUUGCGAGUCUUCAUUUGCAUACGGGCUCUAUAAGUAGCGCAUAACCAGCCCGUUUUGCGGUAGUUCGGAUUACUUCUUUAAGUCUCUUUUCUCUUUUUUCGCGCAAAAAUGCCGGAUCCAGCGAAAUCCGCUCCUGCUCCCAAGAAGGGCUCCAAAAAGGCUGUUACGAAAGUGCAGAAGAAGGACGGCAAGAAGCGCAAGCGCAGCCGCAAGGAGAGCUACUCCGUUUACGUGUACAAGGUGCUGAAGCAGGUCCACCCCGACACCGGCAUCUCGUCCAAGGCCAUGGGCAUCAUGAACUCCUUCGUCAACGACAUCUUCGAGC\n" +
            ">chr1:149784741-149784985(-)\n" +
            "CUUCCAGAGCUCGGCCGUGAUGGCGCUGCAGGAGGCCAGCGAGGCCUACCUGGUGGGGCUGUUCGAAGACACGAACCUGUGCGCCAUCCAUGCCAAGCGCGUGACCAUCAUGCCCAAGGACAUCCAGUUGGCCCGCCGCAUCCGCGGGGAGCGGGCCUAAGGCAUAUUUUUAAGUGGUCGAUCUAAAGGCUCUUUUCAGAGCCACUGCCGUUUUCAUCAAGAGCAGCUGUACCGGCUCUCCAUC\n"
        );
        /*$.ajax({
            $("#inputRNA").val("A");
            url: "examples/example_wo_struct.txt",
            dataType: "text",
            success: function (data) {
                $("#inputRNA").val(data);
            }
        });*/
    });

});