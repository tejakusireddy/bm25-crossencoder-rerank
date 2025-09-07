def query_intersections(self, x_terms=None, y_terms=None, symmetric=False):
        
        if x_terms is None:
            x_terms = []
        if y_terms is None:
            y_terms = []
        xset = set(x_terms)
        yset = set(y_terms)
        zset = xset.union(yset)

        # first built map of gene->termClosure.
        # this could be calculated ahead of time for all g,
        # but this may be space-expensive. TODO: benchmark
        gmap={}
        for z in zset:
            gmap[z] = []
        for subj in self.subjects:
            ancs = self.inferred_types(subj)
            for a in ancs.intersection(zset):
                gmap[a].append(subj)
        for z in zset:
            gmap[z] = set(gmap[z])
        ilist = []
        for x in x_terms:
            for y in y_terms:
                if not symmetric or x<y:
                    shared = gmap[x].intersection(gmap[y])
                    union = gmap[x].union(gmap[y])
                    j = 0
                    if len(union)>0:
                        j = len(shared) / len(union)
                    ilist.append({'x':x,'y':y,'shared':shared, 'c':len(shared), 'j':j})
        return ilist