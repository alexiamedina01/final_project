# src/final_project/hosts.py

from .place import Place

# create the host class
class Host:
    def __init__(self, host_id:int, place:Place, city):
        self.host_id = host_id
        self.city = city
        self.area = place.area
        self.assets = {place.place_id}
        self.profits = 0

# define update_profits
    def update_profits(self):
        for pid in self.assets:
            p = self.city.places[pid]
            self.profits += p.rate * p.occupancy

# define the host's behavior in the property market
    def make_bids(self):
        opportunities = set()
        for pid in self.assets:
            p = self.city.places[pid]
            for nb in p.neighbours:
                if nb not in self.assets:
                    opportunities.add(nb)

        bids = []
        for pid in opportunities:
            place:Place = self.city.places[pid]
            ask_price = place.get_last_sale_price()

            if self.profits >= ask_price:
                bids.append({
                    'place_id': pid,
                    'seller_id': place.host_id,
                    'buyer_id': self.host_id,
                    'spread': self.profits - ask_price,
                    'bid_price': self.profits
                })

        return bids
