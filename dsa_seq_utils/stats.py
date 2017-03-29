#!/usr/bin/env python
from __future__ import division
import math


def calculate_mean(data_list):
    """
    Calculate the mean of a list of numbers.
    :param data_list: List of numbers
    :return: Mean of those numbers.
    """
    if not data_list:
        raise ValueError('At least 1 value is needed to calculate mean.')
    return sum(data_list)/len(data_list)


def calculate_pop_sd(data_list):
    """
    Calculate the population standard deviation of a list of numbers.
    :param data_list: List of numbers.
    :return: The population standard deviation of the list of numbers.
    """
    # Make sure there are enough data points.
    sample_number = len(data_list)
    if sample_number < 2:
        raise ValueError('At least 2 data points needed to calculate population standard deviation.')

    # Get the mean.
    mean = calculate_mean(data_list)
    # Calculate the variance.
    variance = sum(math.pow(j - mean, 2) for j in data_list)/sample_number
    return math.sqrt(variance)


def calculate_median(data_list):
    """
    Calculate the median of a list of numbers.
    :param data_list: List of numbers
    :return: Median of those numbers.
    """
    if not data_list or len(data_list) == 1:
        raise ValueError('At least 2 values are needed to calculate the median.')

    dist_length = len(data_list)
    sorted_data = sorted(data_list)
    if dist_length % 2 == 0:
        x = sorted_data[dist_length//2]
        y = sorted_data[(dist_length//2)-1]
        return (x+y)/2
    else:
        return sorted_data[dist_length//2]