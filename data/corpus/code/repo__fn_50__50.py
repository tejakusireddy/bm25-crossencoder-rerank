@Nonnull
  public static EbInterfaceWriter <Ebi41InvoiceType> ebInterface41 ()
  {
    final EbInterfaceWriter <Ebi41InvoiceType> ret = EbInterfaceWriter.create (Ebi41InvoiceType.class);
    ret.setNamespaceContext (EbInterface41NamespaceContext.getInstance ());
    return ret;
  }