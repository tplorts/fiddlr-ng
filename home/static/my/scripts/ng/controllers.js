'use strict';


var cmod = angular.module('fiddlrApp.controllers', []);


function readScopeInitials(scope) {
    scope.colors = {
        buttons: {
            primary: 'orpheus-purple'
        }
    };
    if( angular.isUndefined(ngScopeInitials) )
        return;
    for( var k in ngScopeInitials ) {
        if( ngScopeInitials.hasOwnProperty(k) ) {
            scope[k] = ngScopeInitials[k];
        }
    }
}        


cmod.controller(
    'CommonHeaderController',
    ['$scope', '$modal', '$position', '$tooltip', '$http',
     function($scope, $modal, $position, $tooltip, $http) {
         readScopeInitials( $scope );

         $scope.openLoginModal = function() {
             var modalInstance = $modal.open({
                 templateUrl: 'login-modal.html',
                 controller: SigninupModalController,
                 size: 'sm'
             });
         };
     } // end: controller function
    ] 
); // end: CommonHeaderController


var SigninupModalController = 
    function ($scope, $modalInstance, $position, $tooltip, $http)
{
    readScopeInitials( $scope );

    $scope.jk = function () {
        $modalInstance.dismiss('cancel');
    };

    // Open the modal with the sign-in page active
    $scope.signinup = {which: 'in'};

    // The pending credentials in the sign-up form
    $scope.pending = {
        username: '',
        password: '',
        email: ''
    };

    $scope.forms = {};
    
    var isUsernameTaken = false;
    var awaitingUsernameCheck = false;
    var usernameTimeout = null;

    // Keep a cache of usernames we've already looked-up
    var checkedUsernames = {};

    function _turnUsernameTooltip( showhide ) {
        $('#signup-username').trigger(showhide+'UsernameTooltip');
    }
    function turnUsernameTooltip( showhide ) {
        setTimeout( function() {
            _turnUsernameTooltip(showhide);
        }, 0);
    }

    function checkUsername() {
        awaitingUsernameCheck = true;
        usernameTimeout = null;
        var u = $scope.pending.username;
        var apiURL = '/custom-api/exists/user/'+u+'/.json';
        var p = $http({method: 'GET', url: apiURL});
        p.success(function(data, status, headers, config) {
            // If the input was changed between issuing the request
            // and receiving a response, then keep awaiting-
            // username-check at true.
            if( !usernameTimeout ) {
                awaitingUsernameCheck = false;
                isUsernameTaken = (data === 'true');
                checkedUsernames[u] = isUsernameTaken;
                if( isUsernameTaken )
                    turnUsernameTooltip('show');
            }
        });
        p.error(function(data, status, headers, config) {
            // called asynchronously if an error occurs
            // or server returns response with an error status.
            console.log('error response from user existence check');
            //TODO: recheck?
        });
    };



    $scope.getUsernameTooltip = function() {
        if( $scope.signinup.which != 'up' ) return '';

        var errors = $scope.forms.signup.username.$error;
        if( errors && errors.pattern )
            return 'please only use letters, numbers, or any of: . - + @ _ (no spaces)';
        if( awaitingUsernameCheck )
            return 'checking that username; please wait a moment';
        if( isUsernameTaken )
            return 'that username is taken; please choose another';
        return '';
    };


    $scope.usernameChanged = function() {
        // Cancel the check-username http request before it issues
        // because the username input has been updated.
        clearTimeout( usernameTimeout );
        usernameTimeout = null;
        awaitingUsernameCheck = false;
        isUsernameTaken = false;

        var u = $scope.pending.username;
        if( $scope.forms.signup.username.$invalid ) {
            turnUsernameTooltip('show');
        } else if( checkedUsernames[u] !== undefined ) {
            isUsernameTaken = checkedUsernames[u];
            if( isUsernameTaken )
                turnUsernameTooltip('show');
        } else {
            turnUsernameTooltip('hide');
            if( u.length > 0 ) {
                // check if available
                usernameTimeout = setTimeout(function() {
                    checkUsername( u );
                }, 500);
            }
        }
    };

    $scope.usernameStatus = function() {
        if( $scope.signinup.which != 'up' ) return '';

        if( $scope.forms.signup.username.$invalid ) 
            return 'has-error';
        var u = $scope.pending.username;
        if( !u.length || usernameTimeout || awaitingUsernameCheck )
            return '';
        if( isUsernameTaken )
            return 'has-warning';
        return 'has-success';
    }

    $scope.usernameIcon = function() {
        if( $scope.signinup.which != 'up' ) return '';

        if( $scope.forms.signup.username.$invalid )
            return 'remove';
        if( usernameTimeout || awaitingUsernameCheck )
            return 'time';
        if( isUsernameTaken )
            return 'warning-sign';
        return 'ok';
    }
};



cmod.controller(
    'FrontPageController', 
    ['$scope', '$position', '$tooltip',
     function($scope, $position, $tooltip) {
         readScopeInitials( $scope );

         $scope.briefs = {
             'Experience': 'Arma virumque cano, Troiae qui primus ab oris Italiam, fato profugus, Laviniaque venit litora, multum ille et terris iactatus et alto vi superum saevae memorem Iunonis ob iram; multa quoque et bello passus, dum conderet urbem, inferretque deos Latio, genus unde Latinum, Albanique patres, atque altae moenia Romae.',
             'Create': 'Musa, mihi causas memora, quo numine laeso, quidve dolens, regina deum tot volvere casus insignem pietate virum, tot adire labores impulerit. Tantaene animis caelestibus irae?',
             'Nexus': 'Urbs antiqua fuit, Tyrii tenuere coloni, Karthago, Italiam contra Tiberinaque longe ostia, dives opum studiisque asperrima belli; quam Iuno fertur terris magis omnibus unam posthabita coluisse Samo; hic illius arma, hic currus fuit; hoc regnum dea gentibus esse, si qua fata sinant, iam tum tenditque fovetque.'
         };
     }
    ]
);



cmod.controller(
    'EditAccountController', 
    ['$scope', '$position', '$tooltip', '$http', '$cookies',
     function($scope, $position, $tooltip, $http, $cookies) {
         readScopeInitials( $scope );

         $scope.isEmailVerified = null;

         $http.post('/custom-api/is-email-verified/', {}, {}).success(
             function(data, status) {
                 $scope.isEmailVerified = data === 'true';
             }
         );

         $scope.isPasswordChangerOpen = false;
         $scope.pw = {
             first: '',
             second: ''
         };
         $scope.pwValid = function() {
             return $scope.pw.first.length > 0 && 
                 $scope.pw.first == $scope.pw.second;
         };
         $scope.pwTooltip = 'Please ensure that the two password fields match';
         $scope.submitNewPassword = function() {
             if( $scope.pwValid() ) {
                 var newPassword = $scope.pw.first;
                 
             }
         };
     }
    ]
);



cmod.controller(
    'ExperienceHomepageController',
    ['$scope', function($scope) {
        readScopeInitials( $scope );
        $scope.menu = {
            isHidden: true
        };
    }]
);


cmod.controller(
    'ExploreController',
    ['$scope', '$http', '$filter', 'Creo', function($scope, $http, $filter, Creo) {
        readScopeInitials( $scope );
        
        $scope.isLoading = true;
        $scope.allCreos = [];
        $scope.creos = {};
        for( var ctype in Creotypes ){
            $scope.creos[parseInt(ctype)] = [];
        }

        function defaultThen(creos) {
            if( $scope.isMapView ){
                $scope.allCreos = _.filter( creos, function(c){
                    return c.hasGeocoordinates();
                });
            } else {
                $scope.allCreos = creos;
            }
            for( var ctype in Creotypes ){
                var iType = parseInt(ctype);
                $scope.creos[iType] = _.where($scope.allCreos, {creotype: iType});
            }
            $scope.isLoading = false;
        }

        function llBox(center, distance) {
            var Root2 = 1.41421356237;
            var NE = center.destinationPoint(45, distance*Root2);
            var dLat = NE.lat - center.lat;
            var dLon = NE.lon - center.lon;
            return {
                latitudeMin: center.lat - dLat,
                latitudeMax: center.lat + dLat,
                longitudeMin: center.lon - dLon,
                longitudeMax: center.lon + dLon
            };
        }

        var I = new LatLon(40.765871,-73.983872);
        var parameterMap = {
            'browse': {},
            'featured': {},
            'nearyou': llBox(I, 3),
            'happeningnow': {creotype: CreotypeEvent},
            'fiddlrevents': {}
        };
        
        Creo.getList(parameterMap[$scope.listKey]).then( defaultThen );

        function nearYouFilter( creo ) {
            var distance = creo.getLatLon().distanceTo(I);
            return distance < 3;
        }


        var creoFilters = {
            'nearyou': nearYouFilter
        };

        $scope.listFilter = function(listKey) {
            if( listKey in creoFilters )
                return creoFilters[listKey];
            return function( creo ) { return true; };
        };

        // Specific to the map view
        $scope.map = {
            center: I,
            zoom: 12
        };

        $scope.hoverMarkerId = null;
        $scope.clickedMarkerId = null;
        $scope.itemStati = {}; // empty is ok: all start closed
        $scope.markerEvents = {
            'mouseover': function(event) {
                var thisMarker = this;
                $scope.$apply(function() {
                    thisMarker.options.opacity = 1;
                    $scope.hoverMarkerId = thisMarker.coords.id;
                });
            },
            'mouseout': function(event) {
                var thisMarker = this;
                $scope.$apply(function() {
                    thisMarker.options.opacity = 0.7;
                    $scope.hoverMarkerId = null;
                });
            },
            'click': function(event) {
                var id = this.coords.id;
                $scope.$apply(function() {
                    $scope.itemStati[id] = true;
                });
            }
        };
    }]
);




cmod.controller(
    'CreoPageController', 
    ['$scope', '$http', '$upload', '$q', 'Creo', 'Location', function($scope, $http, $upload, $q, Creo, Location) {
        readScopeInitials( $scope );
        
        Creo.one($scope.creoId).get().then(function(c){
            $scope.creo = c;
        });

        $scope.creotypeName = function() {
            if( !$scope.creo || angular.isUndefined(Creotypes) )
                return '';
            return Creotypes[$scope.creo.creotype];
        };

        $scope.isGalleriaInitialized = false;

        $scope.openPortfolio = function() {
            if( !$scope.isGalleriaInitialized ) {
                Galleria.loadTheme( GalleriaThemeJs.miniml );
                Galleria.run('.galleria', {
                    imagePan: false,
                    imageCrop: false
                });
                $scope.isGalleriaInitialized = true;
            }
        };

        $scope.bulletin = {
            isOpen: [true, false, false]
        };
        

        // Everthing past this point is only for Create
        if( !$scope.isEditing ) return;
        //=============================================

        $scope.isUploading = {};
        $scope.isPatching = {};

        var uploadPicture = function( fieldName ) {
            $scope.isUploading[fieldName] = true;
            function doneUploading() {
                $scope.isUploading[fieldName] = false;
            }
            var files = pendingFiles[fieldName];
            var cpk = $scope.creo.id;
            for (var i = 0; i < files.length; i++) {
                var file = files[i];
                $scope.upload = $upload.upload({
                    url: '/api/creo/'+cpk+'/uploadCover/.json',
                    file: file,
                    fileFormDataName: fieldName
                }).progress(function(evt) {
                    console.log('percent: ' + parseInt(100.0 * evt.loaded / evt.total));
                }).success(function(data, status, headers, config) {
                    // To keep the Restangularity of creo: extend
                    $scope.creo = angular.extend($scope.creo, data);
                    doneUploading();
                });
                //.error(...)
                //.then(success, error, progress); 
                // access or attach event listeners to the underlying XMLHttpRequest.
                //.xhr(function(xhr){xhr.upload.addEventListener(...)})
            }
        };


        // For each field, by field name, holds whether the editing
        // state is active (true) or inactive (false).
        $scope.editing = {};

        $scope.oldValues = {};

        $scope.beginEditing = function( fieldName ) {
            $scope.editing[fieldName] = true;
            $scope.oldValues[fieldName] = $scope.creo[fieldName];
        };

        var patchableFields = ['name','brief','about','location'];

        $scope.endEditing = function( fieldName ) {
            $scope.editing[fieldName] = false;
            $scope.isMapOpen[fieldName] = false;
            var newValue = $scope.creo[fieldName];
            var hasChanged = newValue !== $scope.oldValues[fieldName];
            if( !hasChanged ) return;

            if( _.contains(patchableFields, fieldName) ){
                var patchData = {};
                patchData[fieldName] = newValue;
                $scope.isPatching[fieldName] = true;
                $scope.creo.patch(patchData).then(function(data) {
                    console.log(data);
                    angular.extend( $scope.creo, data );
                    $scope.isPatching[fieldName] = false;
                });
            } else if( _.contains(['logo','cover'], fieldName) ) {
                uploadPicture( fieldName );
            }
        };

        var pendingFiles = {};
        
        $scope.onFileChanged = function( fieldName, files ) {
            pendingFiles[fieldName] = files;
            // Shouldn't break the view because for example, it
            // uses coverURL instead of cover itself, and we're not
            // changing the __URL field.
            $scope.creo[fieldName] = 'something different';
            // The value doesn't actually matter.
        };

        $scope.gettingLocations = {};


        var getComponent = function(item, compName) {
            return _.find( item.address_components, function(comp){
                return _.contains( comp.types, compName );
            });
        };

        var neighborhoodName = function(item) {
            if( !item ) return;
            var name = getComponent(item, 'neighborhood').long_name;
            var sublo = getComponent(item, 'sublocality_level_1');
            if( sublo ) name += ', ' + sublo.long_name;
            return name;
        };

        var geocoder = new google.maps.Geocoder();

        var getLocations = function(geocodeQuery) {
            var deferred = $q.defer();
            var promise = deferred.promise;
            geocoder.geocode(geocodeQuery, function (results, status) {
                if( status == google.maps.GeocoderStatus.OK ) {
                    deferred.resolve(results);
                } else {
                    deferred.reject(status);
                }
            });
            return promise;
        };//end: getLocations()

        $scope.getNamedLocations = function(typedQuery) {
            return getLocations({
                address: typedQuery,
                componentRestrictions: {
                    locality: 'New York'
                }
            }).then(function(geocoderResults) {
                var nbhoods = [];
                angular.forEach(geocoderResults, function(item){
                    if( _.contains(item.types, 'neighborhood') ){
                        item['neighborhood'] = neighborhoodName(item);
                        nbhoods.push( item );
                    }
                });
                return nbhoods;
            });
        };

        $scope.isPreparingLocation = {};

        $scope.selectLocation = function(fieldName, item) {
            var params = {};
            // TODO: account for things other than neighborhood...
            params['neighborhood'] = item.neighborhood;
            $scope.isPreparingLocation[fieldName] = true;
            Location.getList(params).then(function(locations){
                // console.log('received: '+locations.length+' matches');
                if( locations.length > 0 ) {
                    var l = locations[0];
                    $scope.creo[fieldName] = l.id;
                    $scope.isPreparingLocation[fieldName] = false;
                } else {
                    Location.post({
                        'neighborhood': item.neighborhood
                    }).then(function(loc) {
                        $scope.creo[fieldName] = loc.id;
                        $scope.isPreparingLocation[fieldName] = false;
                    });
                }
            });
        };//end: selectLocation()

        var getMapLocations = function() {
            var c = $scope.map.center;
            getLocations({
                latLng: new google.maps.LatLng(c.latitude, c.longitude)
            }).then(function(geocoderResults) {
                var nbhoods = [];
                angular.forEach(geocoderResults, function(item){
                    if( _.contains(item.types, 'neighborhood') ){
                        item['neighborhood'] = neighborhoodName(item);
                        nbhoods.push( item );
                    }
                });
                $scope.mapLocations = nbhoods;
            });
        };

        $scope.map = {
            center: {
                latitude: 40.7517556,
                longitude: -73.9844816
            },
            zoom: 14,
            events: {
                dragend: getMapLocations
            }
        };
        $scope.isMapOpen = {};
        $scope.hasMapOpened = {};
        $scope.toggleMap = function( fieldName ) {
            $scope.isMapOpen[fieldName] = !$scope.isMapOpen[fieldName];
            if( $scope.isMapOpen[fieldName] ) {
                $scope.hasMapOpened[fieldName] = true;
            }
        }
        $scope.mapLocations = [];

        $scope.clickMapLocation = function( fieldName, i ) {
            var loc = $scope.mapLocations[i];
            var inputKey = fieldName + 'Input';
            $scope.creo[inputKey] = loc.neighborhood;
            $scope.selectLocation( fieldName, loc );
        };
    }] // end: controller function
); // end: CreoPageController









































//    _____ ________________  ____________   _____   ____  _   ________
//   / ___// ____/ ____/ __ \/ ____/_  __/  /__  /  / __ \/ | / / ____/
//   \__ \/ __/ / /   / /_/ / __/   / /       / /  / / / /  |/ / __/   
//  ___/ / /___/ /___/ _, _/ /___  / /       / /__/ /_/ / /|  / /___   
// /____/_____/\____/_/ |_/_____/ /_/       /____/\____/_/ |_/_____/   


cmod.controller(
    'ControllerGabriellae',
    ['$scope', function($scope) {
        $scope.map = {
            center: {
                latitude: 40.7517556,
                longitude: -73.9844816
            },
            zoom: 14
        };
        var coor = function(t) {
            var i = t;
            t *= Math.PI*2 / 30;
            var r = (-73.972315 - -73.996112) / 10;
            var y = r*( 13*Math.cos(t) - 5*Math.cos(2*t) - 2*Math.cos(3*t) - Math.cos(4*t) );
            var x = r*( 16*Math.pow(Math.sin(t), 3) );
            var hCenter = $scope.map.center;
            return {
                id: i,
                latitude: hCenter.latitude + y,
                longitude: hCenter.longitude + x
            };
        };
        $scope.coords = [];
        for( var i=0; i<30; i++ ) {
            $scope.coords.push( coor(i) );
        }
    }]
);

