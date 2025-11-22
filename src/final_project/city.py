# src/final_project/city.py

import pandas as pd
from .place import Place
from .hosts import Host
import random

class City:
    def __init__(self, size, area_rates):
        self.size = size
        self.area_rates = area_rates
        self.step = 0

    def initialize(self):
        # create places
        self.places = []
        for i in range(self.size * self.size):
            p = Place(i, i, self)    # host inicial = place_id
            self.places.append(p)

        # setup de los places
        for p in self.places:
            p.setup()

        # hosts
        self.hosts = []
        for p in self.places:
            h = Host(p.host_id, p, self)
            self.hosts.append(h)

    @property
    def area_mean_rates(self):
        means = {}
        for a in range(4):
            rates = [p.rate for p in self.places if p.area == a]
            means[a] = sum(rates)/len(rates)
        return means

# bids from the hosts; spread of approved transactions
    def approve_bids(self, bids):
        if not bids:
            return []
        df = pd.DataFrame(bids).sort_values("spread", ascending=False)

        bought = set()
        sold = set()
        approved = []

        for _, b in df.iterrows():          # information about the transaction parts
            pid = b["place_id"]
            buy = b["buyer_id"]
            sell = b["seller_id"]

            if pid not in sold and buy not in bought:   # attribute of transaction
                approved.append(b)
                sold.add(pid)
                bought.add(buy)

        return approved     # recive the list

    def execute_transactions(self, transactions):
        for b in transactions:
            pid = int(b["place_id"])
            buyer = self.hosts[int(b["buyer_id"])]
            seller = self.hosts[int(b["seller_id"])]

            price = b["bid_price"]      # amount of money that the buyer is willing to pay

    
            buyer.profits -= price         # profits amount of each host, that starts with 0
            seller.profits += price

            buyer.assets.add(pid)          # if we buy we add the place; if we sell, we lost the place
            seller.assets.remove(pid)

            place = self.places[pid]
            place.host_id = buyer.host_id   # change the host of the place after the transaction
            place.price[self.step] = price

    def clear_market(self):
        bids = []
        for h in self.hosts:
            bids.extend(h.make_bids())

        tx = self.approve_bids(bids)
        self.execute_transactions(tx)
        return tx

    def iterate(self):              # goes to step = 1
        self.step += 1
        for p in self.places:
            p.update_occupancy()
        for h in self.hosts:
            h.update_profits()
        return self.clear_market()
