def serialiseObjectList(objList):
    ser_list = []

    for obj in objList:
        ser_list.append(obj.as_dict())

    return ser_list