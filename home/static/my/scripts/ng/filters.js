'use strict';


var fmod = angular.module('fiddlrApp.filters', []);



fmod.filter('dateRange', ['$filter', function($filter) {
    var ordinalSuffixes = ['th','st','nd','rd'];
    function ordinalSuffix( day ) {
        if( day >= 11 && day <= 13 )
            return 'th';
        var ones = day % 10;
        ones = ones > 3 ? 0 : ones;
        return ordinalSuffixes[ones];
    }
    function superOrdinalSuffix(date) {
        return '<sup>' + ordinalSuffix(date.getDate()) + '</sup>';
    }
    function fTime(date) {
        var fmt = 'h';
        if( date.getMinutes() != 0 )
            fmt += ':mm';
        return $filter('date')(date, fmt+'a').toLowerCase();
    }

    return function(event) {
        var start = new Date(event.start);
        var end = new Date(event.end);
        var sameMonth = start.getMonth() == end.getMonth();
        var sameDay = sameMonth && start.getDate() == end.getDate();

        var from = $filter('date')(start, 'MMM d') + superOrdinalSuffix(start) + ', ' + fTime(start);
        var to = fTime(end);
        if( !sameDay )
            to = $filter('date')(end, 'd') + superOrdinalSuffix(end) + ', ' + to;
        if( !sameMonth )
            to = $filter('date')(end, 'MMM ') + to;
        return from + ' &ndash; ' + to;
    };
}]);



fmod.filter('formattedText', ['$filter', function($filter) {
    return function(rawText) {
        if( !rawText ) return '';
        return rawText.replace(/\n/g, '<br>');
    };
}]);



fmod.filter('default', ['$filter', function($filter) {
    return function(text, defaultValue) {
        return text ? text : defaultValue;
    };
}]);



fmod.filter('pageURL', ['$filter', function($filter) {
    return function(creo) {
        if( !angular.isUndefined(creo) && creo && creo.hasOwnProperty('id') )
            return '/experience/page/' + creo.id + '/';
        return '';
    };
}]);
