def trace(fout=None, format=None, byteorder=sys.byteorder, nanosecond=False):
    
    str_check(fout or '', format or '')
    return TraceFlow(fout=fout, format=format, byteorder=byteorder, nanosecond=nanosecond)