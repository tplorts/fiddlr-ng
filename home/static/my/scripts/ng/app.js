'use strict';


var fiddlrApp = angular.module('fiddlrApp', [
    'google-maps',
    'ui.bootstrap',
    'ngRoute',
    'ngCookies',
    'ngSanitize',
    'fiddlrApp.controllers',
    'fiddlrApp.directives',
    'fiddlrApp.filters'
]).config(
    ['$interpolateProvider', '$tooltipProvider',
     function($interpolateProvider, $tooltipProvider) {
         $interpolateProvider.startSymbol('[[');
         $interpolateProvider.endSymbol(']]');

         $tooltipProvider.setTriggers({
             'mouseenter': 'mouseleave',
             'click': 'click',
             'focus': 'blur',
             'showUsernameTooltip': 'hideUsernameTooltip'
         });
     }]);
