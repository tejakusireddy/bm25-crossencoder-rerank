public void populate(Object target, Map properties) throws BeanMappingException {
        BeanMappingParam param = new BeanMappingParam();
        param.setSrcRef(properties);
        param.setTargetRef(target);
        param.setConfig(this.populateConfig);
        param.setProcesses(BeanMappingEnvironment.getBeanMapVps());
        // 执行mapping处理
        BeanMappingExecutor.execute(param);
    }