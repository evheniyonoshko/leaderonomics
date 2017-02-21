# -*- coding: utf-8 -*-

from iso3166 import countries

__author__ = 'Yevhenii Onoshko'


def generate_country_list():
    choices = []
    for country in countries:
        choices.append((country.alpha2, country.name))
    return tuple(choices)
