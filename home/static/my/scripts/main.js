
$(window).on('load', function() {
    if( loginPrompted ) {
        $('#signinup-modal-button').trigger('click');
    }
});




function deepCopy( obj ) {
    return JSON.parse(JSON.stringify(obj));
}



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
