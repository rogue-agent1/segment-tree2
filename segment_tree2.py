#!/usr/bin/env python3
"""segment_tree2 - Segment tree for range min/max/sum queries."""
import sys, math
class SegTree:
    def __init__(self, arr, op=min, identity=float('inf')):
        self.n = len(arr); self.op = op; self.id = identity
        self.tree = [identity] * (4 * self.n)
        self._build(arr, 1, 0, self.n - 1)
    def _build(self, arr, node, start, end):
        if start == end: self.tree[node] = arr[start]; return
        mid = (start + end) // 2
        self._build(arr, 2*node, start, mid); self._build(arr, 2*node+1, mid+1, end)
        self.tree[node] = self.op(self.tree[2*node], self.tree[2*node+1])
    def query(self, l, r): return self._query(1, 0, self.n-1, l, r)
    def _query(self, node, start, end, l, r):
        if r < start or end < l: return self.id
        if l <= start and end <= r: return self.tree[node]
        mid = (start + end) // 2
        return self.op(self._query(2*node, start, mid, l, r), self._query(2*node+1, mid+1, end, l, r))
    def update(self, idx, val): self._update(1, 0, self.n-1, idx, val)
    def _update(self, node, start, end, idx, val):
        if start == end: self.tree[node] = val; return
        mid = (start + end) // 2
        if idx <= mid: self._update(2*node, start, mid, idx, val)
        else: self._update(2*node+1, mid+1, end, idx, val)
        self.tree[node] = self.op(self.tree[2*node], self.tree[2*node+1])
if __name__ == "__main__":
    arr = [3,1,4,1,5,9,2,6,5,3]
    if len(sys.argv) > 1: arr = [int(x) for x in sys.argv[1].split(",")]
    for name, op, ident in [("Min", min, float('inf')), ("Max", max, float('-inf')), ("Sum", lambda a,b: a+b, 0)]:
        st = SegTree(arr, op, ident)
        print(f"{name} query [2,7]: {st.query(2, 7)}")
    print(f"Array: {arr}")
