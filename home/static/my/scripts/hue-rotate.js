var huerotation = 0;
function hueRotateStep() {
	spinee = $(".hue-rotate");
	spinee.css("-webkit-filter", "hue-rotate(" + huerotation + "deg)");
	huerotation = (huerotation + 3) % 360;
};

setInterval(hueRotateStep, 100);
