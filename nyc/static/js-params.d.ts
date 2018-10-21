import { GeoJsonObject } from "geojson";

export interface JsParams {
  mapboxAccessToken: String;
  origin: [number, number];
  area: GeoJsonObject;
}
