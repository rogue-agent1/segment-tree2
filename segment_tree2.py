import argparse

class SegTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        self._build(data, 1, 0, self.n - 1)

    def _build(self, data, node, start, end):
        if start == end:
            self.tree[node] = data[start]
        else:
            mid = (start + end) // 2
            self._build(data, 2*node, start, mid)
            self._build(data, 2*node+1, mid+1, end)
            self.tree[node] = self.tree[2*node] + self.tree[2*node+1]

    def _query(self, node, start, end, l, r):
        if r < start or end < l: return 0
        if l <= start and end <= r: return self.tree[node]
        mid = (start + end) // 2
        return self._query(2*node, start, mid, l, r) + self._query(2*node+1, mid+1, end, l, r)

    def query(self, l, r): return self._query(1, 0, self.n-1, l, r)

    def _update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = val
        else:
            mid = (start + end) // 2
            if idx <= mid: self._update(2*node, start, mid, idx, val)
            else: self._update(2*node+1, mid+1, end, idx, val)
            self.tree[node] = self.tree[2*node] + self.tree[2*node+1]

    def update(self, idx, val): self._update(1, 0, self.n-1, idx, val)

def main():
    p = argparse.ArgumentParser(description="Segment tree")
    p.add_argument("--demo", action="store_true")
    p.add_argument("--values", nargs="+", type=int)
    args = p.parse_args()
    if args.demo:
        data = [1, 3, 5, 7, 9, 11]
        st = SegTree(data)
        print(f"Data: {data}")
        print(f"Sum [1,3]: {st.query(1, 3)}")
        print(f"Sum [0,5]: {st.query(0, 5)}")
        st.update(2, 10)
        print(f"After update idx 2 = 10:")
        print(f"Sum [1,3]: {st.query(1, 3)}")
    elif args.values:
        st = SegTree(args.values)
        print(f"Sum [0,{len(args.values)-1}]: {st.query(0, len(args.values)-1)}")
    else: p.print_help()

if __name__ == "__main__":
    main()
