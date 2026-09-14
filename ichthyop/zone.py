class Zone(object):

    def __init__(self, index):
        self.name = ''
        self.type = ''
        self.lon = 0
        self.lat = 0
        self.index = index

    def parse_from_ichthyop(self, data):

        coord_v = data[f'coord_zone{self.index}']
        self.name = coord_v.attrs['long_name']
        self.type = coord_v.attrs['type']

        geo_coord = data[f'coord_geo_zone{self.index}']
        self.lon = geo_coord.values[:, 1]
        self.lat = geo_coord.values[:, 0]

    def __str__(self):
        output_string = f'Zone name={self.name}\ntype={self.type}\nlon={self.lon}\nlat={self.lat}'
        return output_string


def parse_zones(data):

    zones = []
    varlist = [v for v in data.variables if v.startswith('coord_zone')]
    index = [int(v.replace('coord_zone', '')) for v in varlist]
    for i in index:
        zone_temp = Zone(i)
        zone_temp.parse_from_ichthyop(data)
        zones.append(zone_temp)
    return zones