def _get_qgen_var(self, generators, base_mva):
        
        Qg = array([g.q / base_mva for g in generators])

        Qmin = array([g.q_min / base_mva for g in generators])
        Qmax = array([g.q_max / base_mva for g in generators])

        return Variable("Qg", len(generators), Qg, Qmin, Qmax)