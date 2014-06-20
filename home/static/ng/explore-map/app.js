'use strict';


// Declare app level module which depends on filters, and services
var exploreApp = angular.module('exploreApp', [
    'google-maps',
    'ui.bootstrap',
    'ngRoute',
    'exploreApp.filters',
    'exploreApp.services',
    'exploreApp.directives',
    'exploreApp.controllers'
]).config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
}]);
