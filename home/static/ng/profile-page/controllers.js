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
        };
    }] // end: controller function
); // end: ProfilePageController
