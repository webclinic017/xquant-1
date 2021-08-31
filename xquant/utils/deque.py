# -*- encoding: utf8 -*-
import numpy as np


class NumPyDeque(object):
    """
    q = NumPyDeque(100)
    """
    def __init__(self, maxlen, dtype=np.float64, cache_factor=3):
        assert(maxlen >= 1)
        self._maxlen = maxlen
        self._dtype = dtype or np.float64
        self._cache_factor = cache_factor or 3
        self._cache_size = int(self._maxlen*self._cache_factor)
        self._data = np.zeros((self._cache_size,), dtype=dtype)
        self._start_idx = 0
        self._end_idx = 0

    def push(self, value):
        if self._end_idx >= self._cache_size:
            num = self._end_idx - self._start_idx
            self._data[:num] = self._data[self._start_idx:self._end_idx]
            self._start_idx = 0
            self._end_idx = num
        self._data[self._end_idx] = value
        self._end_idx += 1
        # shift
        if self._end_idx > self._maxlen:
            self._start_idx += 1

    def pop(self):
        value = self._data[self._start_idx]
        self._start_idx += 1
        return value

    @property
    def maxlen(self):
        return self._maxlen

    @property
    def values(self):
        return self._data[self._start_idx:self._end_idx]

    def __getitem__(self, i):
        return self.values[i]

    def __setitem__(self, i, value):
        self.values[i] = value

    def __len__(self):
        return self._end_idx - self._start_idx

    def __repr__(self):
        return str(self.values)


if __name__ == "__main__":
    if 0:
        q = NumPyDeque(3)
        print(q)
        q.push(1)
        assert(q[0] == 1)
        assert(len(q) == 1)
        print(q)
        q.push(2)
        assert(q[0] == 1)
        assert(q[1] == 2)
        assert(len(q) == 2)
        print(q)
        q.push(3)
        assert(q[0] == 1)
        assert(q[1] == 2)
        assert(q[2] == 3)
        assert(len(q) == 3)
        print(q)
        q.push(4)
        assert(q[0] == 2)
        assert(q[1] == 3)
        assert(q[2] == 4)
        assert(len(q) == 3)
        print(q)
    if 0:
        q = NumPyDeque(2, cache_factor=2)
        q.push(1)
        q.push(2)
        q.push(3)
        q.push(4)
        q.push(5)
        q.push(6)
        print(q)
    if 1:
        q = NumPyDeque(3, cache_factor=2)
        q.push(1)
        q.push(2)
        q.push(3)
        print(q)
        q.pop()
        q.pop()
        print(q)
        print(q[0])
