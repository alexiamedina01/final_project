import random

class Place:
    def __init__(self, place_id:int, host_id:int, city):
        self.place_id = place_id
        self.host_id = host_id
        self.city = city
    
    def setup(self):
        size = self.city.size
        
        x = self.place_id // size
        y = self.place_id % size
        neighbours = []
        for i in range(max(0, x-1), min(size, x+2)):
            for j in range(max(0, y-1), min(size, y+2)):
                if not (i == x and j == y):
                    neighbours.append(i * size + j)
        self.neighbours = neighbours
 
        if x < size/2 and y < size/2:
            self.area = 0
        elif x < size/2 and y >= size/2:
            self.area = 1
        elif x >= size/2 and y < size/2:
            self.area = 2
        else:
            self.area = 3
        
        low, high = self.city.area_rates[self.area]
        self.rate = random.uniform(low, high)
        self.price = {0: 900 * self.rate}
    
    def update_occupancy(self):
        mean_rate = self.city.area_mean_rates[self.area]
        if self.rate > mean_rate:
            self.occupancy = random.randint(5, 15)
        else:
            self.occupancy = random.randint(10, 20)

    def get_last_sale_price(self):
        return list(self.price.values())[-1]