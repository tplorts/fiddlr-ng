'use strict';


var cmod = angular.module('fiddlrApp.controllers', []);


cmod.controller(
    'CommonHeaderController',
    ['$scope', '$modal', '$position', '$tooltip', '$http',
     function($scope, $modal, $position, $tooltip, $http) {
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
    $scope.loginPrompted = loginPrompted !== undefined && loginPrompted;

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
         $scope.briefs = {
             'Explore': 'Arma virumque cano, Troiae qui primus ab oris Italiam, fato profugus, Laviniaque venit litora, multum ille et terris iactatus et alto vi superum saevae memorem Iunonis ob iram; multa quoque et bello passus, dum conderet urbem, inferretque deos Latio, genus unde Latinum, Albanique patres, atque altae moenia Romae.',
             'Create': 'Musa, mihi causas memora, quo numine laeso, quidve dolens, regina deum tot volvere casus insignem pietate virum, tot adire labores impulerit. Tantaene animis caelestibus irae?',
             'Connect': 'Urbs antiqua fuit, Tyrii tenuere coloni, Karthago, Italiam contra Tiberinaque longe ostia, dives opum studiisque asperrima belli; quam Iuno fertur terris magis omnibus unam posthabita coluisse Samo; hic illius arma, hic currus fuit; hoc regnum dea gentibus esse, si qua fata sinant, iam tum tenditque fovetque.'
         };
     }
    ]
);



cmod.controller(
    'EditAccountController', 
    ['$scope', '$position', '$tooltip', '$http', '$cookies',
     function($scope, $position, $tooltip, $http, $cookies) {

         $scope.isEmailVerified = null;

         $http.post('/custom-api/is-email-verified/', {}, {
             xsrfHeaderName: 'X-CSRFToken',
             xsrfCookieName: 'csrftoken'
         }).success(function(data, status) {
             $scope.isEmailVerified = data === 'true';
         });

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
    'EventsListController',
    ['$scope', '$http', '$filter', function($scope, $http, $filter) {
        $scope.events = [];
        $http.get('/api/events/.json').success( function(data, status, headers, config) {
            $scope.events = data.results;
        });
        $scope.eventFilter = function(listName) {
            if( listName == 'near-you' ) {
                var myself = {
                    latitude: 40.767902,
                    longitude: -73.982038
                };
                return function( event ) {
                    var evloc = event.venue.geocoordinates;
                    var distance = geoDistance(evloc, myself);
                    return distance < 2;
                };
            }
            return function( event ) { return true; };
        };
    }]
);




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
        $scope.moveTabPane = function(tabIndex) {
            $('.tab-content').css('margin-left', -tabIndex*100+'%');
            if( tabIndex == 1 && Galleria ) {
                initGalleria();
            }
        };
    }] // end: controller function
); // end: ProfilePageController
