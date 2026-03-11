#!/usr/bin/env python3
"""segment_tree2 — Segment tree for range min/max/sum queries. Zero deps."""

class SegmentTree:
    def __init__(self, arr, op=min, default=float('inf')):
        self.n = len(arr)
        self.op = op
        self.default = default
        self.tree = [default] * (4 * self.n)
        self._build(arr, 1, 0, self.n - 1)

    def _build(self, arr, node, start, end):
        if start == end:
            self.tree[node] = arr[start]
            return
        mid = (start + end) // 2
        self._build(arr, 2*node, start, mid)
        self._build(arr, 2*node+1, mid+1, end)
        self.tree[node] = self.op(self.tree[2*node], self.tree[2*node+1])

    def update(self, idx, val, node=1, start=0, end=None):
        if end is None: end = self.n - 1
        if start == end:
            self.tree[node] = val
            return
        mid = (start + end) // 2
        if idx <= mid:
            self.update(idx, val, 2*node, start, mid)
        else:
            self.update(idx, val, 2*node+1, mid+1, end)
        self.tree[node] = self.op(self.tree[2*node], self.tree[2*node+1])

    def query(self, l, r, node=1, start=0, end=None):
        if end is None: end = self.n - 1
        if r < start or end < l:
            return self.default
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return self.op(
            self.query(l, r, 2*node, start, mid),
            self.query(l, r, 2*node+1, mid+1, end)
        )

def main():
    arr = [1, 3, 5, 7, 9, 11]
    st_min = SegmentTree(arr, min, float('inf'))
    st_sum = SegmentTree(arr, lambda a,b: a+b, 0)
    print(f"Array: {arr}")
    print(f"Range min [1,4]: {st_min.query(1, 4)}")
    print(f"Range sum [1,4]: {st_sum.query(1, 4)}")
    st_min.update(2, 0)
    st_sum.update(2, 0)
    print(f"After arr[2]=0, min [1,4]: {st_min.query(1, 4)}")
    print(f"After arr[2]=0, sum [1,4]: {st_sum.query(1, 4)}")

if __name__ == "__main__":
    main()
