var eventList = null;
var overMarkerClass = 'corresponding-marker-hover';

var item4marker = function( m ) {
    var id = m.coords.id;
    var item = eventList.find('.event-item[geo-id="' + id + '"]');
    return item;
};

var mouseoverMarker = function( event ) {
    item4marker(this).addClass( overMarkerClass );
};

var mouseoutMarker = function( event ) {
    item4marker(this).removeClass( overMarkerClass );
};

var markerEvents = {
    'mouseover': mouseoverMarker,
    'mouseout': mouseoutMarker
};


var mouseoverItem = function( event ) {
    var id = $(this).attr('event-id');
};

var mouseoutItem = function( event ) {
    var id = $(this).attr('event-id');
};

$(document).on('ready', function() {
    eventList = $('.events-map-list');
    eventList.find('.event-item').hover( mouseoverItem, mouseoutItem );
});
