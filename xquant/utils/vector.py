# -*- encoding: utf8 -*-
import math
import numpy as np


class NumPyVector(object):
    """
    [@2021-07-21 23:38:59] cc
    q = NumPyVector(100)
    """
    def __init__(self, capacity=100, dtype=np.float64, grow_factor=2):
        assert(grow_factor >= 1.1)
        assert(capacity >= 1)
        self._dtype = dtype or np.float64
        self._grow_factor = grow_factor or 1.5
        self._size = 0
        self._capacity = capacity
        self._data = np.zeros((self._capacity,), dtype=dtype)

    def append(self, value):
        self.push(value)

    def push(self, value):
        if self._size >= self._capacity:
            self._capacity = math.ceil(self._grow_factor*self._capacity)
            tmp = self._data[:self._size]
            self._data = np.zeros((self._capacity,), dtype=self._dtype)
            self._data[:self._size] = tmp
        self._data[self._size] = value
        self._size += 1

    @property
    def values(self):
        return self._data[:self._size]

    def __getitem__(self, i):
        return self.values[i]

    def __setitem__(self, i, value):
        self.values[i] = value

    def __len__(self):
        return self._size

    @property
    def capacity(self):
        return self._capacity

    def __repr__(self):
        return str(self.values)
