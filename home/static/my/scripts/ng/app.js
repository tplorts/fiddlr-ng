'use strict';


var fiddlrApp = angular.module('fiddlrApp', [
    'google-maps',
    'ui.bootstrap',
    'ngRoute',
    'fiddlrApp.controllers'
]).config(
    ['$interpolateProvider', '$tooltipProvider',
     function($interpolateProvider, $tooltipProvider) {
         $interpolateProvider.startSymbol('[[');
         $interpolateProvider.endSymbol(']]');

         $tooltipProvider.setTriggers({
             'showUsernameTooltip': 'hideUsernameTooltip'
         });
     }]);
