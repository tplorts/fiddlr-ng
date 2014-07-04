// Formulae taken from:
// http://www.movable-type.co.uk/scripts/latlong.html

var EarthRadius = 6371; // km

function deg2rad( deg ) {
    return deg * Math.PI / 180;
}

function haversineDistance(φ1, λ1, φ2, λ2) {
    var Δφ = deg2rad(lat2-lat1);
    var Δλ = deg2rad(lon2-lon1);

    var a = (Math.sin(Δφ/2) * Math.sin(Δφ/2) +
             Math.cos(φ1)  *  Math.cos(φ2) *
             Math.sin(Δλ/2) * Math.sin(Δλ/2));
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

    return EarthRadius * c;
}

// Equirectangular approximation
function equirectDistance(φ1, λ1, φ2, λ2) {
    var x = (λ2-λ1) * Math.cos((φ1+φ2)/2);
    var y = (φ2-φ1);
    var d = Math.sqrt(x*x + y*y) * EarthRadius;
}

function geoDistanceUsing(ll1, ll2, distFn) {
    var φ1 = deg2rad(ll1.latitude);
    var φ2 = deg2rad(ll2.latitude);
    var λ1 = deg2rad(ll1.longitude);
    var λ2 = deg2rad(ll2.longitude);
    return distFn(φ1, λ1, φ2, λ2);
}


function geoDistance(ll1, ll2) {
    var dLat = Math.abs(ll1.latitude - ll2.latitude);
    var dLon = Math.abs(ll1.longitude - ll2.longitude);
    var llThreshold = 1;
    var nearby = dLat < llThreshold && dLon < llThreshold;
    var method = nearby ? equirectDistance : haversineDistance;
    return geoDistanceUsing(ll1, ll2, method);
}

