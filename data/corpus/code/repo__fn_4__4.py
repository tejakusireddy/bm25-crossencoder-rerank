def key_to_kind(cls, key):
    
    if key.kind() == Kind.KIND_NAME:
      return key.id()
    else:
      return key.parent().id()