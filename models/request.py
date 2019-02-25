class Request:
    def __init__(self, kind_premises='', post_code='', region='', city_type='', city='',
                 street_type='', street='', house='', block='', flat='', adress='', try_num=0, id=0):
        self.kind_premises = kind_premises
        self.post_code = post_code
        self.region = region
        self.city_type = city_type
        self.city = city
        self.street_type = street_type
        self.street = street
        self.house = house
        self.block = block
        self.flat = flat
        self.adress = adress
        self.try_num = try_num
        self.id = id


