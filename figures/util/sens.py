#!/usr/bin/env python2
# coding: utf-8

"""Parameters for sensitivity tests."""

configs = ['ccyc4+till1545',
           'ccyc4+rheocp10+till1545',
           'ccyc4+rheocp10+esia5+till1545',
           'ccyc4+d050+wmax05m+till1545',
           'ccyc4+d010+wmax01m+till1545']
labels = ['Default', 'Hard ice', 'Soft ice', 'Hard bed', 'Soft bed']
offsets = [6.2, 6.0, 6.6, 5.9, 6.5]
colors = ['k', '#ff7f00', '#fdbf6f', '#6a3d9a', '#cab2d6']