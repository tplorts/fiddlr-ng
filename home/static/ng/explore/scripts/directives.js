'use strict';

/* Directives */


var dmod = angular.module('exploreApp.directives', []);


dmod.directive('appVersion', ['version', function(version) {
    return function(scope, elm, attrs) {
        elm.text(version);
    };
}]);
