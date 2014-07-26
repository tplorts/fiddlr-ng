'use strict';


var fiddlrApp = angular.module('fiddlrApp', [
    'google-maps',
    'ui.bootstrap',
    'ngRoute',
    'ngCookies',
    'ngSanitize',
    'ngResource',
    'restangular',
    'angularFileUpload',
    'fiddlrApp.controllers',
    'fiddlrApp.directives',
    'fiddlrApp.filters',
    'fiddlrApp.services'
]);

fiddlrApp.config(
    ['$interpolateProvider', '$tooltipProvider', 
     '$httpProvider', '$resourceProvider', 'RestangularProvider',
     function($interpolateProvider, $tooltipProvider, $httpProvider, $resourceProvider, RestangularProvider) {
         $interpolateProvider.startSymbol('[[');
         $interpolateProvider.endSymbol(']]');

         $tooltipProvider.setTriggers({
             'mouseenter': 'mouseleave',
             'click': 'click',
             'focus': 'blur',
             'showUsernameTooltip': 'hideUsernameTooltip'
         });

         $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
         $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
         $httpProvider.defaults.xsrfCookieName = 'csrftoken';

         // Don't strip trailing slashes from calculated URLs
         //$resourceProvider.defaults.stripTrailingSlashes = false;

         RestangularProvider.setBaseUrl('/api');
         RestangularProvider.setRequestSuffix('/.json');
     }
    ]
);
