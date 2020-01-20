$(document).on('submit', '#ccForm', function (event) {
    event.preventDefault();
    convert_currency();
});

function convert_currency() {
    $.ajax({
        url: '/',
        type: "POST",

        data: {
            amount: $('#amount').val(),
            from_currency: $('#from_currency').val(),
            to_currency: $('#to_currency').val(),
            csrfmiddlewaretoken: $('input[name = csrfmiddlewaretoken]').val(),
        },
        success: function (json) {
            console.log(json);
            console.log("success");
            $('#amount').val('');
            $("#result").prepend(json.amount + " " + json.from_currency + " = " + json.result + " " + json.to_currency);
        },

        // handle a non-successful response
        error: function () {
            console.log("ERROR");
        }

    });
}