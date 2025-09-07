def get_labels(self, plt, label_fontsize=10):
        

        # center of vacuum and bulk region
        if len(self.slab_regions) > 1:
            label_in_vac = (self.slab_regions[0][1] + self.slab_regions[1][0])/2
            if abs(self.slab_regions[0][0]-self.slab_regions[0][1]) > \
                    abs(self.slab_regions[1][0]-self.slab_regions[1][1]):
                label_in_bulk = self.slab_regions[0][1]/2
            else:
                label_in_bulk = (self.slab_regions[1][1] + self.slab_regions[1][0]) / 2
        else:
            label_in_bulk = (self.slab_regions[0][0] + self.slab_regions[0][1])/2
            if self.slab_regions[0][0] > 1-self.slab_regions[0][1]:
                label_in_vac = self.slab_regions[0][0] / 2
            else:
                label_in_vac = (1 + self.slab_regions[0][1]) / 2

        plt.plot([0, 1], [self.vacuum_locpot]*2, 'b--', zorder=-5, linewidth=1)
        xy = [label_in_bulk, self.vacuum_locpot+self.ave_locpot*0.05]
        plt.annotate(r"$V_{vac}=%.2f$" %(self.vacuum_locpot), xy=xy,
                     xytext=xy, color='b', fontsize=label_fontsize)

        # label the fermi energy
        plt.plot([0, 1], [self.efermi]*2, 'g--',
                 zorder=-5, linewidth=3)
        xy = [label_in_bulk, self.efermi+self.ave_locpot*0.05]
        plt.annotate(r"$E_F=%.2f$" %(self.efermi), xytext=xy,
                     xy=xy, fontsize=label_fontsize, color='g')

        # label the bulk-like locpot
        plt.plot([0, 1], [self.ave_bulk_p]*2, 'r--', linewidth=1., zorder=-1)
        xy = [label_in_vac, self.ave_bulk_p + self.ave_locpot * 0.05]
        plt.annotate(r"$V^{interior}_{slab}=%.2f$" % (self.ave_bulk_p),
                     xy=xy, xytext=xy, color='r', fontsize=label_fontsize)

        # label the work function as a barrier
        plt.plot([label_in_vac]*2, [self.efermi, self.vacuum_locpot],
                 'k--', zorder=-5, linewidth=2)
        xy = [label_in_vac, self.efermi + self.ave_locpot * 0.05]
        plt.annotate(r"$\Phi=%.2f$" %(self.work_function),
                     xy=xy, xytext=xy, fontsize=label_fontsize)

        return plt