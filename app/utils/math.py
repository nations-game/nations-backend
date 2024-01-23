def clamp(value: float, max: float, min: float):
    if(value > max):
        value = max
    elif(value < min):
        value = min
    return value