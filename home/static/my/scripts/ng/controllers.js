'use strict';


var cmod = angular.module('fiddlrApp.controllers', []);


cmod.controller(
    'CommonHeaderController',
    ['$scope', '$modal', '$position', '$tooltip',
     function($scope, $modal, $position, $tooltip) {
         $scope.openLoginModal = function() {
             var modalInstance = $modal.open({
                 templateUrl: 'login-modal.html',
                 controller: ModalInstanceCtlr,
                 size: 'sm'
             });
         };
     } // end: controller function
    ] 
); // end: CommonHeaderController


var ModalInstanceCtlr = 
    function ($scope, $modalInstance, $position, $tooltip)
{
    $scope.jk = function () {
        $modalInstance.dismiss('cancel');
    };
    $scope.signDirection = 'in';

    $scope.pending = {
        username: '',
        password: ''
    };

    $scope.isUsernameTaken = false;

    $scope.usernameTooltip = '';
    $scope.getUsernameTooltip = function( error ) {
        if( error && error.pattern )
            return 'please only use letters, numbers, or any of: . - + @ _ (no spaces)';
        return '';
    };
    $scope.usernameChanged = function( errors ) {
        $scope.usernameTooltip = $scope.getUsernameTooltip(errors);
        if( $scope.usernameTooltip.length > 0 ) {
            setTimeout( function() {
                $('#signup-username').trigger('showUsernameTooltip');
            }, 0);
        } else {
            // check if available
            setTimeout( function() {
                $('#signup-username').trigger('hideUsernameTooltip');
            }, 0);
        }
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
