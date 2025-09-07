public static <T> T objectFromClause(Class<T> type, String clause, Object... args)
    {
        return SqlClosure.sqlExecute(c -> OrmElf.objectFromClause(c, type, clause, args));
    }