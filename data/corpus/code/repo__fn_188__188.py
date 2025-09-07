public void scalarMultiply(double c)
    {
        int m = rows;
        int n = cols;
        for (int i = 0; i < m; i++)
        {
            for (int j = 0; j < n; j++)
            {
                consumer.set(i, j, c * supplier.get(i, j));
            }
        }
    }