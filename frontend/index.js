import 'ol/ol.css';

import {Tile as TileLayer, Image as ImageLayer, Vector as VectorLayer} from 'ol/layer';
import {OSM, XYZ, Vector as VectorSource, ImageStatic as Static} from 'ol/source';
import {Style, Circle as CircleStyle, Stroke, Fill} from 'ol/style';
import GeoJSONFormat from 'ol/format/GeoJSON';
import Feature from 'ol/Feature';
import {Point} from 'ol/geom';
import Overlay from 'ol/Overlay';
import Map from 'ol/Map';
import View from 'ol/View';
import {getCenter} from 'ol/extent';
import {get as getProjection, transform, Projection, toLonLat} from 'ol/proj';
import {toStringHDMS} from 'ol/coordinate';
import {register} from 'ol/proj/proj4';
import proj4 from 'proj4';

const sensors = {"CAF312": [493947, 5180966]}

proj4.defs("EPSG:26911",
    "+proj=utm +zone=11 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs");
register(proj4);
var proj26911 = getProjection('EPSG:26911');
proj26911.setExtent([-5773188.31, 4213884.46, 869797.41, 9857845.83]);

var extent = [493147, 5180468, 494217, 5181187];
var highlightStyle = new Style({image: new CircleStyle({
  radius: 10,
  fill: new Fill({color: 'rgba(255,255,255,0.7)'}),
  stroke: new Stroke({color: '#CC9933', width: 5}),
})});
var circleStyle = new Style({image: new CircleStyle({
  radius: 10,
  fill: new Fill({color: "rgba(255,255,255,0.4)"}),
  stroke: new Stroke({color: "#CC9933", width: 2.5}),
})});

var sensorsSource = new VectorSource({url: "/sensor_locations.geojson", format: new GeoJSONFormat()});
/*var sensorsSource = new VectorSource();
sensorsSource.addFeature(new Feature({geometry: new Point(sensors["CAF312"]).transform('EPSG:26911', 'EPSG:3857'), locationId: "CAF312"}));*/
var sensorsLayer = new VectorLayer({
  source: sensorsSource,
  //projection: "EPSG:26911",
  style: circleStyle,
});
console.log(sensorsSource);

var container = document.getElementById('popup');
var content = document.getElementById('popup-content');
var overlay = new Overlay({
  element: container,
  autoPan: true,
  autoPanAnimation: {
    duration: 250,
  },
});
var map = new Map({
  layers: [
    new TileLayer({
      source: new XYZ({
        attributions: ['Powered by Esri',
                   'Source: Esri, DigitalGlobe, GeoEye, Earthstar Geographics, CNES/Airbus DS, USDA, USGS, AeroGRID, IGN, and the GIS User Community'],
        url: 'https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        maxZoom: 23
      })
    }),
    new ImageLayer({
      source: new Static({
        //attributions: '© TODO',
        url: '/colormap.png',
        projection: "EPSG:26911",
        imageExtent: extent,
      }),
    }),
    sensorsLayer,
  ],
  overlays: [overlay],
  target: 'map',
  view: new View({
    //center: transform([(extent[0]+extent[2])/2, (extent[1]+extent[3])/2], proj26911, getProjection("EPSG:3857")),
    zoom: 15,
    //projection: "EPSG:3857",
    center: transform(getCenter(extent), proj26911, getProjection("EPSG:3857")),
  }),
});

var selected = null;
map.on('pointermove', function (e) {
  if (selected !== null) {
    selected.setStyle(undefined);
    selected = null;
  }

  map.forEachFeatureAtPixel(e.pixel, function (f) {
    selected = f;
    f.setStyle(highlightStyle);
    return true;
  });

  if (selected) {
    var coordinate = e.coordinate;
    var hdms = toStringHDMS(toLonLat(coordinate));
    content.innerHTML = `<p><b>Sensor ID:</b> ${selected.get("Location")}</p>`;
    overlay.setPosition(coordinate);
  } else {
    overlay.setPosition(undefined);
  }
});
