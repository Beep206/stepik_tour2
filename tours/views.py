import random

from django.http import Http404
from django.shortcuts import render
from django.views import View

from tours.data.data import title, tours, departures
import tours.data.data


class MainView(View):
    def get(self, request, *args, **kwargs):
        index_subtitle = tours.data.data.subtitle
        index_description = tours.data.data.description
        list_tours_id = [key for key in tours.data.data.tours]
        list_random_tours_id = random.sample(list_tours_id, 6)
        random_dict_tours = dict()

        for key, values in tours.data.data.tours.items():
            for num in list_random_tours_id:
                if key == num:
                    random_dict_tours[key] = values

        tours_id = random_dict_tours
        return render(
            request,
            "tour/index.html",
            {
                "index_subtitle": index_subtitle,
                "index_description": index_description,
                "tours_id": tours_id,
                "title": title,
                "departures": departures,
            }
        )


class DepartureView(View):
    def get(self, request, departure, *args, **kwargs):
        if departure not in tours.data.data.departures.keys():
            return Http404

        depart_count = 0
        depart_city = ""
        destination_hotel = dict()
        price = []
        nights = []

        for values in tours.data.data.tours.values():
            if departure == values.get("departure"):
                price.append(values["price"])

        price_min = min(price)
        price_max = max(price)
        price_min = '{:,}'.format(price_min).replace(',', ' ')
        price_max = '{:,}'.format(price_max).replace(',', ' ')

        for values in tours.data.data.tours.values():
            if departure == values.get("departure"):
                nights.append(values["nights"])

        nights_min = min(nights)
        nights_max = max(nights)

        for key, values in tours.data.data.departures.items():
            if key == departure:
                depart_city = values

        for key, values in tours.data.data.tours.items():
            if departure == values.get("departure"):
                depart_count += 1
                destination_hotel[key] = values

        return render(
            request,
            "tour/departure.html",
            {
                "depart_count": depart_count,
                "destination_hotel": destination_hotel,
                "depart_city": depart_city,
                "price_min": price_min,
                "price_max": price_max,
                "nights_min": nights_min,
                "nights_max": nights_max,
                "title": title,
                "departures": departures,
            }
        )


class TourView(View):
    def get(self, request, id, *args, **kwargs):
        tours_id = tours.data.data.tours.get(id)
        tours_stars = "★" * int(tours.data.data.tours.get(id).get("stars"))
        tours_departures = tours.data.data.tours.get(id).get("departure")
        tours_price = tours.data.data.tours.get(id).get("price")
        tours_price = '{:,}'.format(tours_price).replace(',', ' ')
        for key, values in tours.data.data.departures.items():
            if key == tours_departures:
                tours_departures = values
        tours_main_title = tours.data.data.tours.get(id).get("title") + " - " + tours.data.data.title
        return render(
            request,
            "tour/tour.html",
            {
                "tours_id": tours_id,
                "tours_stars": tours_stars,
                "tours_main_title": tours_main_title,
                "tours_departures": tours_departures,
                "tours_price": tours_price,
                "title": title,
                "departures": departures,
            }
        )
