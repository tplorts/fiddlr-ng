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

function HueRotation( selector, rps, increment ) {
    this.element = $(selector);
    this.angle = 0;
    this.angleIncrement = typeof increment === 'undefined' ? 6 : increment;
    var msperrev = 1000 / (typeof rps === 'undefined' ? 0.2 : rps);
    var revsperstep = this.angleIncrement / 360;
    this.intervalTime = msperrev * revsperstep;
    this.intervalId = null;
}

HueRotation.prototype.step = function() {
    this.angle = (this.angle + this.angleIncrement) % 360;
    var filter = 'hue-rotate(' + this.angle + 'deg)';
	this.element.css({
        '-webkit-filter': filter,
        '-moz-filter': filter,
        'filter': filter
    });
};

HueRotation.prototype.start = function() {
    var self = this;
    this.intervalId = setInterval( function() {
        self.step();
    }, this.intervalTime );
};

HueRotation.prototype.stop = function() {
    if( this.intervalId ) {
        clearInterval( this.intervalId );
    }
}

HueRotation.prototype.reset = function() {
    this.angle = 0;
}

