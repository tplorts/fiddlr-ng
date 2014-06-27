
var boogieb;
var boo;
var dball;
var backdrop;
$(window).on('load', function() {
    boogieb = $('.boogie-button');
    boo = document.getElementById('boogieoogieoogie');
    dball = $('#discoball');
    backdrop = $('.disco-backdrop');
    boogieb.click( function() {
        boo.play();
        lowerDiscoball();
    });
});

function lowerDiscoball() {
    backdrop.addClass('black-backdrop');
    dball.addClass('dothedisco');
}

function raiseDiscoball() {
    backdrop.removeClass('black-backdrop');
    dball.removeClass('dothedisco');
}

