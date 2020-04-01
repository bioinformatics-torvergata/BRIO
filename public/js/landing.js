$(function () {

		//format popovers
  		//$('[data-toggle="popover"]').popover();
  		
  		$('#format_pop_1').popover({
  			html: true,
  			content: 'input sequences are accepted in multiFASTA format:\
  			<ul><li>The line containing the name and/or the description of the \
  			sequence starts with a ">";</li><li> \
			The words following the ">" are interpreted as the RNA id;</li><li>\
			The following line should be the RNA nucleotide sequence;</li><li>\
			Any third line is interpreted as secondary structure information (Optional\
			in dot-bracket)</li></ul>\
			<em>(click again to dismiss)</em>',
			placement: 'right'
  		});

  		$(".chosen-select").chosen({
  			no_results_text: "Oops, nothing found!"
		});
});