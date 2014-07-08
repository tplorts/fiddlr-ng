var allCreate;
var allButtons;
var createNav;
var viewCenter;
var navButtons;
var count;
var central;
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
    viewCenter = contentCenter();
    centerButton( centralButton, viewCenter );
    count = navButtons.length;
    var tincr = 2 * Math.PI / count;
    var t0 = Math.PI / 2;
    var radius = 1.5 * navButtons.width();
    for( var i = 0; i < count; i++ ) {
        var b = $(navButtons[i]);
        var t = i * tincr + t0;
        centerButton(b, {
            x: viewCenter.x + radius * Math.cos(t), 
            y: viewCenter.y + radius * Math.sin(t)
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

function centerButtonTexts() {
    $.each( allButtons, function(babymovethat, butt) {
        $(butt).centerText();
    });
}

$(window).on('load', function () {
    allCreate = $('#create-wrapper');
    central = $('#create-something-wrapper');
    centralButton = central.find('#create-something');
    allButtons = allCreate.find('.create-round-button');
    createNav = allCreate.find('#create-navigation');
    navButtons = createNav.find('.create-round-button');
    centerButton( allButtons, contentCenter() );
    centerButtonTexts();
    allCreate.removeClass('invisible');
    setTimeout( initialArrangeButtons, 50 );

    centralButton.on('click', function() {
    });
    $('#create-backdrop').on('click', function() {
    });
});

$(window).on('resize orientationChanged', function() {
    arrangeButtons();
    centerButtonTexts();
});
