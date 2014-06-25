'use strict';


var cmod = angular.module('fiddlrApp.controllers', []);


cmod.controller(
    'CommonHeaderController',
    ['$scope', '$modal', '$position', function($scope, $modal, $position) {
        $scope.openLoginModal = function() {
            var modalInstance = $modal.open({
                templateUrl: 'login-modal.html',
                controller: ModalInstanceCtlr,
                size: 'sm'
            });
        };
    }] // end: controller function
); // end: CommonHeaderController


var ModalInstanceCtlr = function ($scope, $modalInstance) {
    $scope.jk = function () {
        $modalInstance.dismiss('cancel');
    };
    $scope.signDirection = 'in';

    $scope.pending = {
        username: '',
        password: ''
    };

    $scope.isUsernameTaken = false;
    $scope.isUsernameValid = true;
    $scope.isUsernameOK = function() {
        return $scope.isUsernameValid && !$scope.isUsernameTaken;
    }

    $scope.usernameTooltip = function() {
        if( 1 ) {
            return 'looks good';
        } else {
            return 'Please only use letters, numbers, and -+_@';
        }
    };

    $scope.checkUsername = function( inputObject ) {
        $scope.pendingUsername = inputObject.$viewValue;
    };
};



cmod.controller(
    'ExploreMapController', 
    ['$scope', function($scope) {
        $scope.map = {
            center: {
                latitude: 40.7590615,
                longitude: -73.969231
            },
            zoom: 12
        };

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
); // end: ExploreMapController



cmod.controller(
    'ProfilePageController', 
    ['$scope', function($scope) {
        $scope.alertMe = function() {
            setTimeout(function() {
                alert('You\'ve selected the alert tab!');
            });
        };
        $scope.moveTabPane = function(tabIndex) {
            $('.tab-content').css('margin-left', -tabIndex*100+'%');
            if( tabIndex == 1 && Galleria ) {
                initGalleria();
            }
        };
    }] // end: controller function
); // end: ProfilePageController
