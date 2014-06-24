var majorDiv;
var allButtons;
var createNav;
var center;
var navButtons;
var count;
var centralButton;

function contentSize() {
    return {
        width: $(window).width(),
        height: $(window).height() - $('#header').height()
    };
}

function contentCenter() {
    var s = contentSize();
    return {
        x: s.width / 2,
        y: s.height / 2
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
    centerButton( centralButton, center );
    count = navButtons.length;
    var tincr = 2 * Math.PI / count;
    var t0 = Math.PI / 2;
    var size = contentSize();
    var space = Math.min(size.width, size.height);
    var radius = space/2 - 0.7*navButtons.width();
    for( var i = 0; i < count; i++ ) {
        var b = $(navButtons[i]);
        var t = i * tincr + t0;
        centerButton(b, {
            x: center.x + radius * Math.cos(t), 
            y: center.y + radius * Math.sin(t)
        });
    }
};

(function( $ ){
   $.fn.centerText = function() {
       var text = this.find('.button-text');
       var offset = (this.height() - text.height()) / 2;
       text.css('margin', offset+'px 0');
   };
})( jQuery );


function initialArrangeButtons() {
    arrangeButtons();
    setTimeout(function() {
        createNav.removeClass('prearranged');},
               820);
}

$(window).on('load', function () {
    majorDiv = $('#major-button-div');
    allButtons = majorDiv.find('.circle-button');
    allButtons.centerText();
    createNav = majorDiv.find('#create-navigation');
    navButtons = createNav.find('.circle-button');
    centralButton = majorDiv.find('#create-button');
    centerButton( allButtons, contentCenter() );
    majorDiv.removeClass('invisible');
    setTimeout( initialArrangeButtons, 50 );

    centralButton.on('click', function() {
        centralButton.addClass( 'pending-choice' );
    });
    $('#create-backdrop').on('click', function() {
        centralButton.removeClass('pending-choice');
    });
});

$(window).on('resize orientationChanged', function() {
    arrangeButtons();
    allButtons.centerText();
});
