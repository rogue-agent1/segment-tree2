#!/usr/bin/env python3
"""segment_tree2 - Segment tree with lazy propagation."""
import sys, argparse, json

class SegmentTree:
    def __init__(self, data, op=min, identity=float("inf")):
        self.n = len(data); self.op = op; self.identity = identity
        self.tree = [identity] * (4 * self.n); self.lazy = [0] * (4 * self.n)
        self._build(data, 1, 0, self.n - 1)
    def _build(self, data, node, start, end):
        if start == end: self.tree[node] = data[start]; return
        mid = (start + end) // 2
        self._build(data, 2*node, start, mid)
        self._build(data, 2*node+1, mid+1, end)
        self.tree[node] = self.op(self.tree[2*node], self.tree[2*node+1])
    def _push(self, node, start, end):
        if self.lazy[node]:
            mid = (start + end) // 2
            self._apply(2*node, start, mid, self.lazy[node])
            self._apply(2*node+1, mid+1, end, self.lazy[node])
            self.lazy[node] = 0
    def _apply(self, node, start, end, val):
        self.tree[node] += val; self.lazy[node] += val
    def update_range(self, l, r, val):
        self._update(1, 0, self.n-1, l, r, val)
    def _update(self, node, start, end, l, r, val):
        if r < start or end < l: return
        if l <= start and end <= r: self._apply(node, start, end, val); return
        self._push(node, start, end)
        mid = (start + end) // 2
        self._update(2*node, start, mid, l, r, val)
        self._update(2*node+1, mid+1, end, l, r, val)
        self.tree[node] = self.op(self.tree[2*node], self.tree[2*node+1])
    def query(self, l, r):
        return self._query(1, 0, self.n-1, l, r)
    def _query(self, node, start, end, l, r):
        if r < start or end < l: return self.identity
        if l <= start and end <= r: return self.tree[node]
        self._push(node, start, end)
        mid = (start + end) // 2
        return self.op(self._query(2*node, start, mid, l, r), self._query(2*node+1, mid+1, end, l, r))
    def point_update(self, idx, val):
        self._point_update(1, 0, self.n-1, idx, val)
    def _point_update(self, node, start, end, idx, val):
        if start == end: self.tree[node] = val; return
        mid = (start + end) // 2
        if idx <= mid: self._point_update(2*node, start, mid, idx, val)
        else: self._point_update(2*node+1, mid+1, end, idx, val)
        self.tree[node] = self.op(self.tree[2*node], self.tree[2*node+1])

class SumTree(SegmentTree):
    def __init__(self, data): super().__init__(data, op=lambda a,b: a+b, identity=0)
    def _apply(self, node, start, end, val):
        self.tree[node] += val * (end - start + 1); self.lazy[node] += val

def main():
    p = argparse.ArgumentParser(description="Segment tree")
    p.add_argument("--demo", action="store_true")
    args = p.parse_args()
    if args.demo:
        data = [1,3,5,7,9,11,2,4,6,8]
        print("=== Min Segment Tree ===")
        st = SegmentTree(data)
        print(f"Min [2,7]: {st.query(2,7)}")
        st.point_update(4, 1)
        print(f"After update idx 4 to 1, min [2,7]: {st.query(2,7)}")
        print("\n=== Sum Segment Tree ===")
        sst = SumTree(data)
        print(f"Sum [0,4]: {sst.query(0,4)}")
        sst.update_range(1, 5, 10)
        print(f"After +10 to [1,5], sum [0,4]: {sst.query(0,4)}")
    else: p.print_help()
if __name__ == "__main__": main()
