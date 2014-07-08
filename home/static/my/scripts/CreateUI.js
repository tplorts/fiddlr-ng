var Create = {
    contentSize: function() {
        return {
            width: $(window).width(),
            height: $(window).height() - $('#header').height()
        };
    },
    contentCenter: function() {
        var s = this.contentSize();
        return {
            x: s.width / 2,
            y: s.height / 2
        };
    },
    placeButton: function( button, itsCenter ) {
        var y = itsCenter.y - button.height() / 2;
        var x = itsCenter.x - button.width() / 2;
        button.css({
            'bottom': y+'px',
            'left': x+'px'
        });
    },
    vCenterText: function( button ) {
        var text = button.find('.button-text');
        var offset = (button.height() - text.height()) / 2;
        text.css('margin', offset+'px 0');
    }
};

function CreateUI( createWrapperSelector ) {
    this.wrapper = $(createWrapperSelector);
    this.central = $('#create-something-wrapper');
    this.centralButton = this.central.find('#create-something');
    this.allButtons = this.wrapper.find('.create-round-button');
    this.createNav = this.wrapper.find('#create-navigation');
    this.navButtons = this.createNav.find('.create-round-button');
    this.navCount = this.navButtons.length;
    Create.placeButton( this.allButtons, Create.contentCenter() );
    this.vCenterBTexts();
    this.wrapper.removeClass('invisible');
    var self = this;
    setTimeout( function() {
        self.initialArrangeButtons();
    }, 50 );

    // this.centralButton.on('click', showCreateSomething);
    // $('#create-backdrop').on('click', hideCreateSomething);
}

CreateUI.prototype.arrangeButtons = function() {
    var viewCenter = Create.contentCenter();
    Create.placeButton( this.centralButton, viewCenter );
    var tincr = 2 * Math.PI / this.navCount;
    var t0 = Math.PI / 2;
    var radius = 1.5 * this.navButtons.width();
    for( var i = 0; i < this.navCount; i++ ) {
        var b = $(this.navButtons[i]);
        var t = i * tincr + t0;
        Create.placeButton(b, {
            x: viewCenter.x + radius * Math.cos(t), 
            y: viewCenter.y + radius * Math.sin(t)
        });
    }
};

CreateUI.prototype.initialArrangeButtons = function() {
    this.arrangeButtons();
    var self = this;
    setTimeout( function() {
        self.createNav.removeClass('prearranged');
    }, 1000);
}

CreateUI.prototype.vCenterBTexts = function() {
    $.each( this.allButtons, function(babymovethat, butt) {
        Create.vCenterText( $(butt) );
    });
};



function showCreateSomething() {
}
function hideCreateSomething() {
}



var createUI;
$(window).on('load', function () {
    createUI = new CreateUI('#create-wrapper');
});

$(window).on('resize orientationChanged', function() {
    createUI.arrangeButtons();
    createUI.vCenterBTexts();
});
