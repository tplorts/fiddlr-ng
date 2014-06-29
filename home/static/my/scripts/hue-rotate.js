var huerotation = 0;
function hueRotateStep() {
	var spinee = $('.hue-rotate');
	huerotation = (huerotation + 3) % 360;
    var filter = 'hue-rotate(' + huerotation + 'deg)';
	spinee.css({
        '-webkit-filter': filter,
        '-moz-filter': filter,
        'filter': filter
    });
};

setInterval(hueRotateStep, 100);
