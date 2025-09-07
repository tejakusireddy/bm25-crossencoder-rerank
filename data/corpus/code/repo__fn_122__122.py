void buildCSSTypesDictionary()
  {
    String description;
    String value;
    TextSearchDictionaryEntry de;


    //search eval() expression
    description = "text/css";
    value = "text/css";
    de = new TextSearchDictionaryEntry(description, value, MessageId.CSS_009);
    v.add(de);


  }