'use strict';


var smod = angular.module('fiddlrApp.services', ['ngResource']);

smod.factory('Artist', ['$resource', function($resource) {
    return $resource('/api/artists/:pk.json', {}, {
    });
}]);

