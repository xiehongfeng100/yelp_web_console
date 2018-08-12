# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from scipy import spatial

from math import *


YELP_LV_BIZES = pd.read_csv('dataset/las_vegas_business_preprocessed_with_db_id.csv')


class KDTreeUtil(object):
    """
    Ref: https://github.com/qingkaikong/blog/tree/master/2017_33_kdtree_2_real_distance
    """

    def __init__(self):
        x, y, z = zip(*map(self.to_Cartesian, YELP_LV_BIZES.latitude.values, YELP_LV_BIZES.longitude.values))
        coordinates = list(zip(x, y, z))
        self.tree = spatial.cKDTree(coordinates)

    def query_by_dist(self, lat, lon, dist=2):
        dist = self.kmToDIST(dist)
        x_ref, y_ref, z_ref = self.to_Cartesian(lat, lon)
        indexes = self.tree.query_ball_point((x_ref, y_ref, z_ref), dist)
        bizes = YELP_LV_BIZES[YELP_LV_BIZES.index.isin(indexes)]
        return bizes.db_id.values.tolist()

    def query_closest(self, lat, lon, limit=10):
        x_ref, y_ref, z_ref = self.to_Cartesian(lat, lon)
        dist, indexes = self.tree.query((x_ref, y_ref, z_ref), limit)
        dist = map(self.distToKM, dist)
        bizes = YELP_LV_BIZES[YELP_LV_BIZES.index.isin(indexes)]
        return [dict(db_id=db_id, popularity=popularity, dist=d)
                for db_id, popularity, d in zip(bizes.db_id.values, bizes.popularity.values, dist)]

    @classmethod
    def to_Cartesian(cls, lat, lng):
        """
        function to convert latitude and longitude to 3D cartesian coordinates
        """
        R = 6371  # radius of the Earth in kilometers

        x = R * cos(lat) * cos(lng)
        y = R * cos(lat) * sin(lng)
        z = R * sin(lat)
        return x, y, z

    @classmethod
    def rad2deg(cls, rad):
        """
        function to convert radian to degree
        """
        degree = rad / 2 / np.pi * 360
        return degree

    @classmethod
    def deg2rad(cls, degree):
        """
        function to convert degree to radian
        """
        rad = degree * 2 * np.pi / 360
        return rad

    @classmethod
    def kmToDIST(cls, x):
        """
        function to convert real distance in km to cartesian distance
        """
        R = 6371  # earth radius
        gamma = 2 * np.arcsin(x / 2. / R)
        dist = 2 * R * cls.rad2deg(sin(gamma / 2.))
        return dist

    @classmethod
    def distToKM(cls, x):
        """
        function to convert cartesian distance to real distance in km
        """
        R = 6371  # earth radius
        gamma = 2 * np.arcsin(cls.deg2rad(x / (2 * R)))  # compute the angle of the isosceles triangle
        dist = 2 * R * sin(gamma / 2)  # compute the side of the triangle
        return dist
