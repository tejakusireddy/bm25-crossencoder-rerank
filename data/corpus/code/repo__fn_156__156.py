def unique_bits(flags_class):
    
    flags_class = unique(flags_class)
    other_bits = 0
    for name, member in flags_class.__members_without_aliases__.items():
        bits = int(member)
        if other_bits & bits:
            for other_name, other_member in flags_class.__members_without_aliases__.items():
                if int(other_member) & bits:
                    raise ValueError("%r: '%s' and '%s' have overlapping bits" % (flags_class, other_name, name))
        else:
            other_bits |= bits