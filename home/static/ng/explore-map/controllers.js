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

        if( initialMarkers !== undefined ) {
            $scope.markers = initialMarkers;
        }
        if( initialEvents !== undefined ) {
            $scope.events = initialEvents;
            for( var i=0; i<$scope.events.length; i++ ) {
                var e = $scope.events[i];
                var geo = e.fields.venue.fields.geocoordinates.fields;
                e['coords'] = {
                    'id': e.pk,
                    'latitude': geo.latitude,
                    'longitude': geo.longitude
                };
            }
        }

        $scope.markerEvents = markerEvents;
    }] // end: controller function
); // end: ExploreController
