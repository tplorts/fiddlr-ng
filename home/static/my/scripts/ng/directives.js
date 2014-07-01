'use strict';


var dmod = angular.module('fiddlrApp.directives', []);



dmod.directive('fiddlrTooltipIfOverflow', function() {
    return {
        restrict: 'A',
        link: function(scope, element) {
            var r = element[0].offsetWidth - element[0].children[0].offsetWidth;
            if( r < 0 )
                console.log('too small: '+r);
        }
    };
});
