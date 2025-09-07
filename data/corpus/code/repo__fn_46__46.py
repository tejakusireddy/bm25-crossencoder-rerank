List<JCClassDecl> listClasses(List<JCCompilationUnit> trees) {
        List<JCClassDecl> result = new ArrayList<>();
        for (JCCompilationUnit t : trees) {
            for (JCTree def : t.defs) {
                if (def.hasTag(JCTree.Tag.CLASSDEF))
                    result.add((JCClassDecl)def);
            }
        }
        return result;
    }