class Pattern:

    def __init__(self, 
            region, group_size, home_owner, car_age,
            car_value, risk_factor, age_oldest, age_youngest,
            married_couple, c_previous, duration_previous, coverages):
        """
            coverages is a dictionary for each coverage type.
            car_value is a letter only for the selected car value, the
                        rest are marked as 0.
        """
        self.region         = region
        self.group_size     = group_size
        self.home_owner     = home_owner
        self.car_age        = car_age
        self.car_value      = car_value
        self.risk_factor    = risk_factor
        self.age_oldest     = age_oldest
        self.age_youngest   = age_youngest
        self.married_couple = married_couple
        self.c_previous     = c_previous
        self.duration_previous = duration_previous
        self.coverages      = coverages
    
    def get_pattern_array(self):
        pattern = []
        pattern.append(int(self.group_size))
        pattern.append(int(self.home_owner))
        pattern.append(int(self.car_age))
        pattern.append(int(self.risk_factor))
        pattern.append(int(self.age_oldest))
        pattern.append(int(self.age_youngest))
        pattern.append(int(self.married_couple))
        pattern.append(int(self.c_previous))
        pattern.append(int(self.duration_previous))
        
        # Sorted as they appear on the dataframe
        car_values = ['f','d','e','h','g','c','i','a','b']
        for cv in car_values:
            pattern.append(int(cv == self.car_value))
        
        # Sorted as they appear on the dataframe
        regions = ["South", "Northeast", "West", "Midwest"]
        for r in regions:
            pattern.append(int(r == self.region))
        
        covs = {
                'A': ['0', '2', '1'] ,
                'B': ['0', '1'],
                'C': ['1', '2', '3','4'],
                'D': ['1', '3', '2'],
                'E': ['0', '1'],
                'F': ['0', '3', '2','1'],
                'G': ['4', '2', '3', '1']
                }
        for c in covs:
            for cov in covs[c]:
                pattern.append(int(cov == self.coverages[c]))
                
        return pattern

