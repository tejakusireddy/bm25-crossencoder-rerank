private void synchronizeElement(
        CmsObject cms,
        String elementPath,
        Collection<String> skipPaths,
        Locale sourceLocale) {

        if (elementPath.contains("/")) {
            String parentPath = CmsXmlUtils.removeLastXpathElement(elementPath);
            List<I_CmsXmlContentValue> parentValues = getValuesByPath(parentPath, sourceLocale);
            String elementName = CmsXmlUtils.getLastXpathElement(elementPath);
            for (I_CmsXmlContentValue parentValue : parentValues) {
                String valuePath = CmsXmlUtils.concatXpath(parentValue.getPath(), elementName);
                boolean skip = false;
                for (String skipPath : skipPaths) {
                    if (valuePath.startsWith(skipPath)) {
                        skip = true;
                        break;
                    }
                }
                if (!skip) {
                    if (hasValue(valuePath, sourceLocale)) {
                        List<I_CmsXmlContentValue> subValues = getValues(valuePath, sourceLocale);
                        removeSurplusValuesInOtherLocales(elementPath, subValues.size(), sourceLocale);
                        for (I_CmsXmlContentValue value : subValues) {
                            if (value.isSimpleType()) {
                                setValueForOtherLocales(cms, value, CmsXmlUtils.removeLastXpathElement(valuePath));
                            } else {
                                List<I_CmsXmlContentValue> simpleValues = getAllSimpleSubValues(value);
                                for (I_CmsXmlContentValue simpleValue : simpleValues) {
                                    setValueForOtherLocales(cms, simpleValue, parentValue.getPath());
                                }
                            }
                        }
                    } else {
                        removeValuesInOtherLocales(valuePath, sourceLocale);
                    }
                }
            }
        } else {
            if (hasValue(elementPath, sourceLocale)) {
                List<I_CmsXmlContentValue> subValues = getValues(elementPath, sourceLocale);
                removeSurplusValuesInOtherLocales(elementPath, subValues.size(), sourceLocale);
                for (I_CmsXmlContentValue value : subValues) {
                    if (value.isSimpleType()) {
                        setValueForOtherLocales(cms, value, null);
                    } else {
                        List<I_CmsXmlContentValue> simpleValues = getAllSimpleSubValues(value);
                        for (I_CmsXmlContentValue simpleValue : simpleValues) {
                            setValueForOtherLocales(cms, simpleValue, null);
                        }
                    }
                }
            } else {
                removeValuesInOtherLocales(elementPath, sourceLocale);
            }
        }
    }