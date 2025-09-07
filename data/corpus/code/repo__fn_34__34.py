private void setJCRProperties(NodeImpl parent, Properties props) throws Exception
   {
      if (!parent.isNodeType("dc:elementSet"))
      {
         parent.addMixin("dc:elementSet");
      }

      ValueFactory vFactory = parent.getSession().getValueFactory();
      LocationFactory lFactory = parent.getSession().getLocationFactory();

      for (Entry entry : props.entrySet())
      {
         QName qname = (QName)entry.getKey();
         JCRName jcrName = lFactory.createJCRName(new InternalQName(qname.getNamespace(), qname.getName()));

         PropertyDefinitionData definition =
            parent
               .getSession()
               .getWorkspace()
               .getNodeTypesHolder()
               .getPropertyDefinitions(jcrName.getInternalName(), ((NodeData)parent.getData()).getPrimaryTypeName(),
                  ((NodeData)parent.getData()).getMixinTypeNames()).getAnyDefinition();

         if (definition != null)
         {
            if (definition.isMultiple())
            {
               Value[] values = {createValue(entry.getValue(), vFactory)};
               parent.setProperty(jcrName.getAsString(), values);
            }
            else
            {
               Value value = createValue(entry.getValue(), vFactory);
               parent.setProperty(jcrName.getAsString(), value);
            }
         }
      }
   }