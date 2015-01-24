#!/usr/bin/python
# coding: utf8

import re
from base import Base


class Arcgis(Base):
    """
    ArcGIS REST API
    =======================
    The World Geocoding Service finds addresses and places in all supported countries
    from a single endpoint. The service can find point locations of addresses,
    business names, and so on.  The output points can be visualized on a map,
    inserted as stops for a route, or loaded as input for a spatial analysis.
    an address, retrieving imagery metadata, or creating a route.

    API Reference
    -------------
    https://developers.arcgis.com/rest/geocode/api-reference/geocoding-find.htm

    OSM Quality (1/6)
    -----------------
    [ ] addr:housenumber
    [ ] addr:street
    [ ] addr:city
    [ ] addr:state
    [ ] addr:country
    [x] addr:postal

    Attributes (12/18)
    ------------------
    [ ] accuracy
    [x] address
    [x] bbox
    [ ] city
    [x] confidence
    [ ] country
    [ ] housenumber
    [x] lat
    [x] lng
    [x] location
    [x] ok
    [x] postal
    [x] provider
    [x] quality
    [x] score
    [ ] state
    [x] status
    [ ] street
    """
    provider = 'arcgis'
    method = 'geocode'

    def __init__(self, location, **kwargs):
        self.url = 'http://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/find'
        self.location = location
        self.params = {
            'f': 'json',
            'text': location,
            'maxLocations': 1,
        }
        self._initialize(**kwargs)

    def _exceptions(self):
        if self.parse['locations']:
            self._build_tree(self.parse['locations'][0])

    @property
    def lat(self):
        return self.parse['geometry']['y']

    @property
    def lng(self):
        return self.parse['geometry']['x']

    @property
    def address(self):
        return self.parse['name']

    @property
    def housenumber(self):
        return ''

    @property
    def street(self):
        return ''

    @property
    def city(self):
        return ''

    @property
    def state(self):
        return ''

    @property
    def country(self):
        return ''

    @property
    def score(self):
        return self.parse['attributes']['Score']

    @property
    def quality(self):
        return self.parse['attributes']['Addr_Type']

    @property
    def postal(self):
        if self.address:
            expression = r'(\d{5}(-\d{4})?)|([ABCEGHJKLMNPRSTVXY]{1}\d{1}[A-Z]{1}( *\d{1}[A-Z]{1}\d{1})?)'
            pattern = re.compile(expression)
            match = pattern.search(self.address.upper())
            if match:
                return match.group(0)

    @property
    def bbox(self):
        south = self.parse['extent']['ymin']
        west = self.parse['extent']['xmin']
        north = self.parse['extent']['ymax']
        east = self.parse['extent']['xmax']
        return self._get_bbox(south, west, north, east)


if __name__ == '__main__':
    g = Arcgis('453 Booth, Ottawa, ON')
    g.debug()