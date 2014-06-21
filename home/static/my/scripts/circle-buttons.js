var center;
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

$(window).on('load resize orientationChanged', function() {
    center = contentCenter();
    var buttons = $('#create-navigation .circle-button');
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
});
