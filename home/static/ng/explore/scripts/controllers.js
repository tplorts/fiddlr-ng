'use strict';

/* Controllers */

var cmod = angular.module('exploreApp.controllers', []);

cmod.controller(
    'ExploreController', 
    ['$scope', function($scope) {
        $scope.map = {
            center: {
                latitude: 40.7590615,
                longitude: -73.969231
            },
            zoom: 12
        };
    }] // end: controller function
); // end: ExploreController