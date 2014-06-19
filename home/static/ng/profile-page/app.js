'use strict';


var profilePageApp = angular.module('profilePageApp', [
    'ui.bootstrap',
    'profilePageApp.controllers'
]).config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
}]);
