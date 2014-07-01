
var soulfood;
$(window).on('load', function() {
    soulfood = document.getElementById('soulfoodhaaappy');
    $('.signout-button').click( function() {
        soulfood.play();
        return false;
    });
    $('#soulfoodhaaappy').on('ended', function() {
        document.getElementById('signout-form').submit();
    });
});
