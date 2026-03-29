#!/usr/bin/env python3
"""Segment tree with lazy propagation for range queries and updates."""
import sys

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self._build(arr, 1, 0, self.n - 1)
    def _build(self, arr, node, start, end):
        if start == end:
            self.tree[node] = arr[start]
            return
        mid = (start + end) // 2
        self._build(arr, 2*node, start, mid)
        self._build(arr, 2*node+1, mid+1, end)
        self.tree[node] = self.tree[2*node] + self.tree[2*node+1]
    def _push(self, node, start, end):
        if self.lazy[node]:
            self.tree[node] += self.lazy[node] * (end - start + 1)
            if start != end:
                self.lazy[2*node] += self.lazy[node]
                self.lazy[2*node+1] += self.lazy[node]
            self.lazy[node] = 0
    def update_range(self, l, r, val):
        self._update(1, 0, self.n-1, l, r, val)
    def _update(self, node, start, end, l, r, val):
        self._push(node, start, end)
        if r < start or end < l: return
        if l <= start and end <= r:
            self.lazy[node] += val
            self._push(node, start, end)
            return
        mid = (start + end) // 2
        self._update(2*node, start, mid, l, r, val)
        self._update(2*node+1, mid+1, end, l, r, val)
        self.tree[node] = self.tree[2*node] + self.tree[2*node+1]
    def query(self, l, r):
        return self._query(1, 0, self.n-1, l, r)
    def _query(self, node, start, end, l, r):
        self._push(node, start, end)
        if r < start or end < l: return 0
        if l <= start and end <= r: return self.tree[node]
        mid = (start + end) // 2
        return self._query(2*node, start, mid, l, r) + self._query(2*node+1, mid+1, end, l, r)

def test():
    st = SegTree([1, 3, 5, 7, 9, 11])
    assert st.query(0, 5) == 36
    assert st.query(1, 3) == 15
    st.update_range(1, 3, 10)  # add 10 to indices 1-3
    assert st.query(1, 3) == 45
    assert st.query(0, 0) == 1
    assert st.query(0, 5) == 66
    print("  segment_tree2: ALL TESTS PASSED")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Segment Tree with lazy propagation")
