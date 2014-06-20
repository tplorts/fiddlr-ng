'use strict';

var cmod = angular.module('profilePageApp.controllers', []);

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
                console.log('init galleria');
                initGalleria();
            }
        };
    }] // end: controller function
); // end: ProfilePageController
