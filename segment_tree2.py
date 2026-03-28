#!/usr/bin/env python3
"""Segment Tree with lazy propagation — zero-dep."""

class SegmentTree:
    def __init__(self, arr):
        self.n=len(arr); self.tree=[0]*(4*self.n); self.lazy=[0]*(4*self.n)
        self._build(arr,1,0,self.n-1)
    def _build(self, arr, node, start, end):
        if start==end: self.tree[node]=arr[start]; return
        mid=(start+end)//2
        self._build(arr,node*2,start,mid); self._build(arr,node*2+1,mid+1,end)
        self.tree[node]=self.tree[node*2]+self.tree[node*2+1]
    def _push_down(self, node, start, end):
        if self.lazy[node]:
            mid=(start+end)//2
            self._apply(node*2,start,mid,self.lazy[node])
            self._apply(node*2+1,mid+1,end,self.lazy[node])
            self.lazy[node]=0
    def _apply(self, node, start, end, val):
        self.tree[node]+=val*(end-start+1); self.lazy[node]+=val
    def update_range(self, l, r, val):
        self._update(1,0,self.n-1,l,r,val)
    def _update(self, node, start, end, l, r, val):
        if r<start or end<l: return
        if l<=start and end<=r: self._apply(node,start,end,val); return
        self._push_down(node,start,end); mid=(start+end)//2
        self._update(node*2,start,mid,l,r,val); self._update(node*2+1,mid+1,end,l,r,val)
        self.tree[node]=self.tree[node*2]+self.tree[node*2+1]
    def query(self, l, r):
        return self._query(1,0,self.n-1,l,r)
    def _query(self, node, start, end, l, r):
        if r<start or end<l: return 0
        if l<=start and end<=r: return self.tree[node]
        self._push_down(node,start,end); mid=(start+end)//2
        return self._query(node*2,start,mid,l,r)+self._query(node*2+1,mid+1,end,l,r)

if __name__=="__main__":
    arr=[1,3,5,7,9,11]
    st=SegmentTree(arr)
    print(f"Array: {arr}")
    print(f"Sum [1..3]: {st.query(1,3)}")
    st.update_range(1,4,10)
    print(f"After +10 to [1..4], sum [1..3]: {st.query(1,3)}")
    print(f"Total sum [0..5]: {st.query(0,5)}")
