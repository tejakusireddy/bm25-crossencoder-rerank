@Override
	public boolean removeArc(int x, int y, ICause cause) throws ContradictionException {
		assert cause != null;
		if (LB.arcExists(x, y)) {
			this.contradiction(cause, "remove mandatory arc " + x + "->" + y);
			return false;
		}
		if (UB.removeArc(x, y)) {
			if (reactOnModification) {
				delta.add(x, GraphDelta.AR_TAIL, cause);
				delta.add(y, GraphDelta.AR_HEAD, cause);
			}
			GraphEventType e = GraphEventType.REMOVE_ARC;
			notifyPropagators(e, cause);
			return true;
		}
		return false;
	}