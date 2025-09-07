public double[] solve(double[] b) {
    if(b.length != L.length) {
      throw new IllegalArgumentException(ERR_MATRIX_DIMENSIONS);
    }
    if(!isspd) {
      throw new ArithmeticException(ERR_MATRIX_NOT_SPD);
    }
    // Work on a copy!
    return solveLtransposed(solveLInplace(copy(b)));
  }