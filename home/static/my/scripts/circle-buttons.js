var createNav;
var center;
var buttons;
var count;

function contentCenter() {
    var hh = $('#header').height();
    var Y = $(window).height() - hh;
    var X = $(window).width();
    return {
        x: X / 2,
        y: hh + Y / 2
    };
}

function centerButton( button, itsCenter ) {
    var y = itsCenter.y - button.height() / 2;
    var x = itsCenter.x - button.width() / 2;
    button.css({
        'bottom': y+'px',
        'left': x+'px'
    });
}




var arrangeButtons = function() {
    center = contentCenter();
    count = buttons.length;
    var tincr = 2 * Math.PI / count;
    var t0 = Math.PI / 2;
    var radius = Math.min(center.x, center.y) - buttons.width();
    center.y -= $('#header').height();
    for( var i = 0; i < count; i++ ) {
        var b = $(buttons[i]);
        var t = i * tincr + t0;
        var x = radius * Math.cos(t) + center.x;
        var y = radius * Math.sin(t) + center.y;
        centerButton(b, {x:x, y:y});
    }
};

function initialArrangeButtons() {
    arrangeButtons();
    setTimeout(function() {
        createNav.removeClass('prearranged');},
               405);
}

$(window).on('load', function () {
    createNav = $('#create-navigation');
    buttons = createNav.find('.circle-button');
    centerButton( buttons, contentCenter() );
    createNav.removeClass('hidden');
    setTimeout( initialArrangeButtons, 10 );
});

$(window).on('resize orientationChanged', arrangeButtons);
