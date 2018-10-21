// @ts-check

/**
 * Get the JS params for this page that were given to us by
 * our back-end and embedded in the page.
 * 
 * @returns {import('./js-params').JsParams}
 */
function getJsParams() {
  const id = 'js-params';
  const el = document.getElementById(id);

  if (!el) {
    throw new Error(`could not find ${id}`);
  }

  return JSON.parse(el.textContent);
}

const jsParams = getJsParams();

const map = L.map('map').setView(jsParams.origin, 13);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
  maxZoom: 18,
  id: 'mapbox.streets',
  accessToken: jsParams.mapboxAccessToken
}).addTo(map);

L.geoJSON(jsParams.area).addTo(map);

const originMarker = L.marker(jsParams.origin).addTo(map);
const targetMarker = L.marker(jsParams.target).addTo(map);

// TODO: Escape the text, looks like it's evaluated as HTML.
originMarker.bindPopup(jsParams.originName);
targetMarker.bindPopup(jsParams.targetName).openPopup();
