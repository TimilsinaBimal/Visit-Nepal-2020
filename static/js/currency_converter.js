$(document).on('submit', '#ccForm', function (event) {
	event.preventDefault();
	$('#result').val('Fetching...');
	convert_currency();
});

function convert_currency () {
	$.ajax({
		url     : '/',
		type    : 'POST',
		data    : {
			amount              : $('#amount').val(),
			from_currency       : $('#from_currency').val(),
			to_currency         : $('#to_currency').val(),
			csrfmiddlewaretoken : $('input[name = csrfmiddlewaretoken]').val()
		},
		success : function (json) {
			console.log(json);
			console.log('success');
			$('#amount').empty();
			$('#result').val(json.result);
		},

		// handle a non-successful response
		error   : function () {
			console.log('Error Ocuured!');
			$('#result').val('Error Occured! Please try again!');
		}
	});
}
