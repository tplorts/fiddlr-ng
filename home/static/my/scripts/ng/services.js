'use strict';


var smod = angular.module('fiddlrApp.services', ['restangular']);

smod.service('Creo', ['Restangular', function(Restangular) {
    var Creo = Restangular.service('creo');
    
    Restangular.extendModel('creo', function(model) {
        model.isArtist = function() {
            return this.creotype === CreotypeArtist;
        };
        model.isVenue = function() {
            return this.creotype === CreotypeVenue;
        };
        model.isSponsor = function() {
            return this.creotype === CreotypeSponsor;
        };
        model.isEvent = function() {
            return this.creotype === CreotypeEvent;
        };
        model.isTour = function() {
            return this.creotype === CreotypeTour;
        };

        model.mapLink = function() {
            if( !this.location ) return '#';
            var mapQuery = this.location.address;
            return 'http://maps.google.com/?q=' + mapQuery;
        };

        return model;
    });

    return Creo;
}]);

