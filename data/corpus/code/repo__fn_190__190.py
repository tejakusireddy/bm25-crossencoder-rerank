private AFPChain alignRight(Atom[] ca1, Atom[] ca2, CECPParameters cpparams)
			throws StructureException {
		long startTime = System.currentTimeMillis();

		Atom[] ca2m = StructureTools.duplicateCA2(ca2);

		if(debug) {
			System.out.format("Duplicating ca2 took %s ms\n",System.currentTimeMillis()-startTime);
			startTime = System.currentTimeMillis();
		}

		// Do alignment
		AFPChain afpChain = super.align(ca1, ca2m,params);

		// since the process of creating ca2m strips the name info away, set it explicitely
		try {
			afpChain.setName2(ca2[0].getGroup().getChain().getStructure().getName());
		} catch( Exception e) {}

		if(debug) {
			System.out.format("Running %dx2*%d alignment took %s ms\n",ca1.length,ca2.length,System.currentTimeMillis()-startTime);
			startTime = System.currentTimeMillis();
		}
		afpChain = postProcessAlignment(afpChain, ca1, ca2m, calculator, cpparams);

		if(debug) {
			System.out.format("Finding CP point took %s ms\n",System.currentTimeMillis()-startTime);
			startTime = System.currentTimeMillis();
		}

		return afpChain;
	}