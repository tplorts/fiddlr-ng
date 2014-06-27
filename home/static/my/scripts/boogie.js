
var boogieb;
var boo;
var dball;
var backdrop;
var isDiscoing = false;

$(window).on('load', function() {
    boogieb = $('.boogie-button');
    boo = document.getElementById('boogieoogieoogie');
    dball = $('#discoball');
    backdrop = $('.disco-backdrop');
    boogieb.click( function() {
        if( !isDiscoing ) {
            boo.play();
        }
        isDiscoing = true;
        lowerDiscoball();
    });
    $('#boogieoogieoogie').on('ended', function() {
        raiseDiscoball();
        isDiscoing = false;
    });
});

function lowerDiscoball() {
    backdrop.css('transition-delay', '0s');
    dball.css('transition-delay', '3s');

    backdrop.addClass('black-backdrop');
    dball.addClass('dothedisco');
}

function raiseDiscoball() {
    backdrop.css('transition-delay', '6s');
    dball.css('transition-delay', '0s');

    backdrop.removeClass('black-backdrop');
    dball.removeClass('dothedisco');
}

