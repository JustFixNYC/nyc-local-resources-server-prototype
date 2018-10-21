import { GeoJsonObject } from "geojson";

export interface JsParams {
  mapboxAccessToken: String;
  origin: [number, number];
  originName: string;
  target: [number, number];
  targetName: string;
  area: GeoJsonObject;
}
