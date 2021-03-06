
$(window).on('load', function() {
    if( loginPrompted ) {
        $('#signinup-modal-button').trigger('click');
        $('#auxiliary-signinup-button').click( function() {
            $('#signinup-modal-button').trigger('click');
        });
        setTimeout( function() {
            $('#please-login').removeClass('invisible');
        }, 1000 );
    }
});




function deepCopy( obj ) {
    return JSON.parse(JSON.stringify(obj));
}

function range(start, stop, step){
    if (typeof stop=='undefined'){
        // one param defined
        stop = start;
        start = 0;
    };
    if (typeof step=='undefined'){
        step = 1;
    };
    if ((step>0 && start>=stop) || (step<0 && start<=stop)){
        return [];
    };
    var result = [];
    for (var i=start; step>0 ? i<stop : i>stop; i+=step){
        result.push(i);
    };
    return result;
};



//=================================================================
// Source: http://css-tricks.com/snippets/jquery/smooth-scrolling/
$(function() {
    $('a.smooth-page-scroll[href*=#]:not([href=#])').click(function() {
        if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
            if (target.length) {
                $('html,body').animate({
                    scrollTop: target.offset().top
                }, 1000);
                return false;
            }
        }
    });
});



/*
  var gradientTopMarkup = '\
  <div class="gradient-border top-edge"></div>\
  ';
  var gradientMarkup = '\
  <div class="gradient-border top-edge"></div>\
  <div class="gradient-border bottom-edge"></div>\
  <div class="gradient-border topright-corner"><div></div></div>\
  <div class="gradient-border right-edge"></div>\
  <div class="gradient-border bottomright-corner"><div></div></div>\
  <div class="gradient-border bottomleft-corner"><div></div></div>\
  <div class="gradient-border left-edge"></div>\
  <div class="gradient-border topleft-corner"><div></div></div>\
  ';

(function( $ ){
   $.fn.gradientBorderTop = function() {
       this.append(gradientTopMarkup);
   };
})( jQuery );
  $(window).on('load', function() {
    $('.pallet-label > .label-inner').gradientBorderTop();
  });
*/



var GabysBirthday = $('#GabysBirthday');
if( GabysBirthday.length == 1 ) {
    console.log('Happy Birthday, Dearest Gaby!');
    var bdaySong = GabysBirthday.find('audio');
    var cake = GabysBirthday.find('img');
    var loadingbit = GabysBirthday.find('.loading-bit');
    bdaySong.on('playing', function() {
        loadingbit.addClass('hidden');
        cake.removeClass('hidden');
    });
    bdaySong.on('ended', function() {
        GabysBirthday.addClass('hidden');
    });
    bdaySong[0].play();
}
