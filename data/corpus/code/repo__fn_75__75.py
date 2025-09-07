def almost_unitary(gate: Gate) -> bool:
    """"""
    res = (gate @ gate.H).asoperator()
    N = gate.qubit_nb
    return np.allclose(asarray(res), np.eye(2**N), atol=TOLERANCE)