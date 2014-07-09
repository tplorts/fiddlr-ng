'use strict';


var fiddlrApp = angular.module('fiddlrApp', [
    'google-maps',
    'ui.bootstrap',
    'ngRoute',
    'ngCookies',
    'ngSanitize',
    'ngResource',
    'fiddlrApp.controllers',
    'fiddlrApp.directives',
    'fiddlrApp.filters',
    'fiddlrApp.services'
]);

fiddlrApp.config(
    ['$interpolateProvider', '$tooltipProvider', 
     '$httpProvider', '$resourceProvider',
     function($interpolateProvider, $tooltipProvider, $httpProvider, $resourceProvider) {
         $interpolateProvider.startSymbol('[[');
         $interpolateProvider.endSymbol(']]');

         $tooltipProvider.setTriggers({
             'mouseenter': 'mouseleave',
             'click': 'click',
             'focus': 'blur',
             'showUsernameTooltip': 'hideUsernameTooltip'
         });

         $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';

         // Don't strip trailing slashes from calculated URLs
         //$resourceProvider.defaults.stripTrailingSlashes = false;
     }
    ]
);

fiddlrApp.run( function($http, $cookies) {
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.xsrfCookieName = 'csrftoken';
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
});
