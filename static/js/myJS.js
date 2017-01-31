$(function() {
    $('#btnSignUp').click(function() {
        console.log('button hit');
        $.ajax({
            url: '/join',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                console.log('success!!!');
            },
            error: function(error) {
                console.log(error);
                console.log('failuree');
            }
        });
    });
});