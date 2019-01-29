#!/bin/env python3

from google.transit import gtfs_realtime_pb2
from ftplib import FTP
import csv
import time

bus_stops = "stops.txt"
bus_url = "ztp.krakow.pl"
bus_file = "VehiclePositions_A.pb"
trips = "trips.txt"
feed = gtfs_realtime_pb2.FeedMessage()

class Bus:
    bus_info = b""
    def __call__(self, chunk=b""):
        self.bus_info += chunk
    def clear(self):
        self.bus_info = b""

def createBusStopsDict(path):
    with open(path, 'r') as f:
        stops = csv.reader(f, delimiter=',')
        x = dict(((row[0], row[2])for row in stops))
        x['stop_0_0'] = "Brak danych"
        return x

def createLineNumberDict(path):
    with open(path, 'r') as f:
        trips = csv.reader(f, delimiter=',')
        x = dict(((row[0], row[1].split('_')[1]) for row in trips))
        return x

if __name__ == "__main__":
    bus = Bus()
    stops = createBusStopsDict(bus_stops)
    lines = createLineNumberDict(trips)

    while True:
        bus.clear()
        # Start FTP
        res = FTP(bus_url)
        res.login()
        res.retrbinary('RETR '+bus_file, bus)
        res.quit()
        # Close FTP

        feed.ParseFromString(bus.bus_info)
        for entity in feed.entity:
            if entity.HasField("vehicle"):
                try:
                    test = lines[entity.vehicle.trip.trip_id]
                    print("-----")
                    print("Linia: "+str(lines[entity.vehicle.trip.trip_id]))
                    print("-----")
                    print("Wysokość: "+str(entity.vehicle.position.latitude))
                    print("Szerokość: "+str(entity.vehicle.position.longitude))
                    print("-----")
                    print("Przystanek: "+str(stops[entity.vehicle.stop_id]))
                    print("-----")
                    print("-----")
                    print()
                except KeyError:
                    continue
                
        time.sleep(60)
