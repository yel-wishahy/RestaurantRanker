#!/usr/bin/env python

#Author: Yousif El-Wishahy
import googlemaps
import numpy as np

#goolge api key
api_key = 'enter key here'
gmaps = googlemaps.Client(key=api_key)

def get_places_dict(queries):
    out = list()
    for q in queries:
        out.append(gmaps.places(q)['results'][0])
    return out

def rank_places(origin,queries,time_limit=60*60,weight=[1/3,1/3,1/3]):
    places = get_places_dict(queries)
    destinations = []
    for place in places:
        destinations.append(place['formatted_address'])
        
    matrix = gmaps.distance_matrix(origin,destinations,mode="transit")
    rank_dict = {}
    for i in range(len(matrix['destination_addresses'])):
        key = 'name: ' + places[i]['name'] + ', address: ' + matrix['destination_addresses'][i]
        
        duration = np.interp(matrix['rows'][0]['elements'][i]['duration']['value'], [0,time_limit],[weight[0]*5,0])
        rating = np.interp(places[i]['rating'], [0,5],[0,weight[1]*5])
        total_ratings = np.interp(places[i]['user_ratings_total'], [0,3000],[0,weight[2]*5])
        
        rank_dict[key] = duration + rating + total_ratings
    
    return dict(sorted( rank_dict.items(), key=lambda item: item[1]))

#example query for fried chicken places
origin= 'Richmond–Brighouse station, Richmond, BC V6Y 2B3' #origin at local skytrain station

queries = ['down low chicken shack commerical', #list of destinations, fried chicken restaurants
          'down low chicken shack ubc',
          'juke chicken vancouver downtown',
          'win win chicken vancouver',
          'chicko chicken vancouver marine drive',
          'chicko chicken vancouver dunbar',
           'chicko chicken burnaby',
          'ole chicken vancouver downtown',
          'nene chicken vancouver',
          'hi five chicken vancouver marine drive']

#run algorithm
ranks = rank_places(origin,queries,time_limit=2*60*60,weight=[0.25,0.5,0.25])

#print results
print(ranks)
