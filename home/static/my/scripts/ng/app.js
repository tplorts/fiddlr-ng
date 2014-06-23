'use strict';


var fiddlrApp = angular.module('fiddlrApp', [
    'google-maps',
    'ui.bootstrap',
    'ngRoute',
    'fiddlrApp.controllers'
]).config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
}]);
