'use strict';


var smod = angular.module('fiddlrApp.services', ['restangular']);

smod.service('Creo', ['Restangular', function(Restangular) {
    var Creo = Restangular.service('creo');
    
    Restangular.extendModel('creo', function(model) {
        model.pageURL = function() {
            return '/experience/page/'+this.id+'/';
        };

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
        
        model.venue = function() {
            return _.findWhere( this.ties, {creotype: CreotypeVenue} );
        };
        model.artists = function() {
            return _.where( this.ties, {creotype: CreotypeArtist} );
        };

        model.locationInfo = function() {
            if( this.locationExpanded ) 
                return this.locationExpanded;
            if( this.isEvent() )
                return this.venue().locationExpanded;
            return null;
        }
        model.latitude = function() {
            return this.locationInfo().latitude;
        };
        model.longitude = function() {
            return this.locationInfo().longitude;
        };
        model.getLatLon = function() {
            return new LatLon(this.latitude(), this.longitude());
        };

        model.mapLink = function() {
            var location = this.locationInfo();
            if( !location ) return '#';
            var mapQuery = location.address;
            return 'http://maps.google.com/?q=' + mapQuery;
        };

        return model;
    });

    return Creo;
}]);





smod.service('Location', ['Restangular', function(Restangular) {
    var Location = Restangular.service('location');
    return Location;
}]);
