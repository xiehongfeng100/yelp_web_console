# -*- coding: utf-8 -*-
import numpy as np
from math import sin, cos
from scipy import spatial
from utils import YELP_LV_BIZES, Utils


class _TransformUtils(object):
    """
    Codes in this class are taken from https://github.com/qingkaikong/blog/tree/master/2017_33_kdtree_2_real_distance
    """

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


# Initialize a global KdTree
X, Y, Z = zip(*map(_TransformUtils.to_Cartesian, YELP_LV_BIZES.latitude.values, YELP_LV_BIZES.longitude.values))
KdTree = spatial.cKDTree(list(zip(X, Y, Z)))


class KdTreeUtils(object):

    @classmethod
    def query_closest(cls, lat, lon, limit=10):
        x_ref, y_ref, z_ref = _TransformUtils.to_Cartesian(lat, lon)
        dist, indexes = KdTree.query((x_ref, y_ref, z_ref), limit)
        dist = map(_TransformUtils.distToKM, dist)
        bizes = YELP_LV_BIZES[YELP_LV_BIZES.index.isin(indexes)]
        return [dict(db_id=db_id,
                     name=Utils.get_biz_name_by_id(db_id),
                     popularity=round(popularity, 2),
                     sentiment=Utils.get_biz_sentiment(db_id),
                     dist=round(d, 2))
                for db_id, popularity, d in zip(bizes.db_id.values, bizes.popularity.values, dist)]

    @classmethod
    def km_between_two_points(cls, lat0, lon0, lat1, lon1):
        x0, y0, z0 = _TransformUtils.to_Cartesian(lat0, lon0)
        x1, y1, z1 = _TransformUtils.to_Cartesian(lat1, lon1)
        return round(_TransformUtils.distToKM(np.sqrt(np.power(x0 - x1, 2) + np.power(y0 - y1, 2) + np.power(z0 - z1, 2))), 2)
