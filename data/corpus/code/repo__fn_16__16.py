def p44(msg):
    
    d = hex2bin(data(msg))

    if d[34] == '0':
        return None

    p = bin2int(d[35:46])    # hPa

    return p