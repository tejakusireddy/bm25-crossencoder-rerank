@SuppressWarnings("unchecked")
	public <T> void sort(Arr arr, Comparator<T> c) {
		int l = arr.getLength();
		Object[] objs = new Object[l];
		for (int i=0; i<l; i++) {
			objs[i] = arr.get(i);
		}
		Arrays.sort((T[])objs, c);
		for (int i=0; i<l; i++) {
			arr.put(i, objs[i]);
		}
	}