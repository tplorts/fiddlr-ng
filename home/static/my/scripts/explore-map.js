var projectList = null;
var overMarkerClass = 'corresponding-marker-hover';

var mouseoverMarker = function( event ) {
    var id = this.coords.id;
    var item = projectList.find('.project-item[project-id="'+id+'"]');
    item.addClass( overMarkerClass );
};

var mouseoutMarker = function( event ) {
    var id = this.coords.id;
    var item = projectList.find('.project-item[project-id="'+id+'"]');
    item.removeClass( overMarkerClass );
};

var markerEvents = {
    'mouseover': mouseoverMarker,
    'mouseout': mouseoutMarker
};


var mouseoverItem = function( event ) {
    var id = $(this).attr('project-id');
};

var mouseoutItem = function( event ) {
    var id = $(this).attr('project-id');
};

$(window).on('load', function() {
    projectList = $('#featured-projects');

    projectList.find('.project-item').hover(
        mouseoverItem, mouseoutItem );
});
