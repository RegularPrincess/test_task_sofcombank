class SearchForm:
    """
    Представляет form-data для запросов на сайт
    """
    def __init__(self, macroRegionId='', regionId='', settlementId='',
                 streetType='', street='', house='', structure='',
                 building='', apartment='', method='searchByAddress'):
        self.macroRegionId = macroRegionId
        self.regionId = regionId
        self.settlementId= settlementId
        self.streetType = streetType
        self.street = street
        self.house = house
        self.structure = structure
        self.building = building
        self.apartment = apartment
        self.method = method
