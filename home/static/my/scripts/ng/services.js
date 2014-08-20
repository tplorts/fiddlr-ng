'use strict';


var smod = angular.module('fiddlrApp.services', ['restangular']);

smod.service('Creo', ['Restangular', function(Restangular) {
    var Creo = Restangular.service('creo');
    
    Restangular.extendModel('creo', function(creoModel) {
        creoModel.pageURL = function() {
            return '/experience/page/'+this.id+'/';
        };

        creoModel.isArtist = function() {
            return this.creotype === CreotypeArtist;
        };
        creoModel.isVenue = function() {
            return this.creotype === CreotypeVenue;
        };
        creoModel.isSponsor = function() {
            return this.creotype === CreotypeSponsor;
        };
        creoModel.isEvent = function() {
            return this.creotype === CreotypeEvent;
        };
        creoModel.isTour = function() {
            return this.creotype === CreotypeTour;
        };
        
        creoModel.venue = function() {
            return _.findWhere( this.ties, {creotype: CreotypeVenue} );
        };
        creoModel.artists = function() {
            return _.where( this.ties, {creotype: CreotypeArtist} );
        };

        creoModel.locationInfo = function() {
            if( this.locationExpanded ) 
                return this.locationExpanded;
            if( this.isEvent() )
                return this.venue().locationExpanded;
            return null;
        }
        creoModel.latitude = function() {
            return this.locationInfo().latitude;
        };
        creoModel.longitude = function() {
            return this.locationInfo().longitude;
        };
        creoModel.getLatLon = function() {
            return new LatLon(this.latitude(), this.longitude());
        };

        creoModel.mapURL = function() {
            var location = this.locationInfo();
            if( !location ) return '#';
            var mapQuery = location.address;
            return 'http://maps.google.com/?q=' + mapQuery;
        };

        return creoModel;
    });

    return Creo;
}]);





smod.service('Location', ['Restangular', function(Restangular) {
    var Location = Restangular.service('location');
    return Location;
}]);
