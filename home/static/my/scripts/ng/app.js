'use strict';


var fiddlrApp = angular.module('fiddlrApp', [
    'google-maps',
    'ui.bootstrap',
    'ngRoute',
    'fiddlrApp.controllers',
    'ngCookies'
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
