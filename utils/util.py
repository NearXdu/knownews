



def listToStr(keywords):
    result = ''
    for word in keywords:
        result += word
        result += ','
    return result[0:len(result)-1]



def strToList(keywords):
    return keywords.split(',')

