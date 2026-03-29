#!/usr/bin/env python3
"""Segment tree — range queries and point updates in O(log n)."""
import sys

class SegTree:
    def __init__(self, data, fn=min, default=float('inf')):
        self.n = len(data); self.fn, self.default = fn, default
        self.tree = [default]*(4*self.n)
        self._build(data, 1, 0, self.n-1)
    def _build(self, data, node, l, r):
        if l == r: self.tree[node] = data[l]; return
        m = (l+r)//2
        self._build(data, 2*node, l, m); self._build(data, 2*node+1, m+1, r)
        self.tree[node] = self.fn(self.tree[2*node], self.tree[2*node+1])
    def _query(self, node, l, r, ql, qr):
        if qr < l or r < ql: return self.default
        if ql <= l and r <= qr: return self.tree[node]
        m = (l+r)//2
        return self.fn(self._query(2*node, l, m, ql, qr), self._query(2*node+1, m+1, r, ql, qr))
    def query(self, l, r): return self._query(1, 0, self.n-1, l, r)
    def _update(self, node, l, r, i, val):
        if l == r: self.tree[node] = val; return
        m = (l+r)//2
        if i <= m: self._update(2*node, l, m, i, val)
        else: self._update(2*node+1, m+1, r, i, val)
        self.tree[node] = self.fn(self.tree[2*node], self.tree[2*node+1])
    def update(self, i, val): self._update(1, 0, self.n-1, i, val)

def main():
    arr = [1, 3, 5, 7, 9, 11]
    st = SegTree(arr); print(f"Array: {arr}")
    print(f"Min [1..4]: {st.query(1,4)}")
    st.update(3, 2); print(f"After update [3]=2, Min [1..4]: {st.query(1,4)}")
    st2 = SegTree(arr, fn=lambda a,b: a+b, default=0)
    print(f"Sum [0..5]: {st2.query(0,5)}")

if __name__ == "__main__": main()
