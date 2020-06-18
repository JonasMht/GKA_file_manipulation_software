from parameters import * #import the parameters.py file

### Functions ###

def SortCrescent(li, index): 
    """Sort a list in a crescent order by the elements located at the index position"""
    return(sorted(li, key = lambda x: x[index]))

def FindIndexByName(name, l):
    """
    In the prismParam list l find and return the index of the element that contains the correct name
    """
    pos = 0
    for e in l:
        if e[0]==name:
            return pos
        pos+=1
    return None

def FindValueByName(name, l):
    """
    In the prismParam list l find and return the value that is linked to the name
    """
    for e in l:
        if e[0]==name:
            return e[1]
    return None

def ChangeValueByName(name, n, l):
    """
    In the prismParam list l change the value that is linked to the name to n
    """
    for e in l:
        if e[0]==name:
            e[1] = n

def gps_to_dt(gpsweek,gpsseconds):
    """Return the conversion of a GPS date to datetime"""
    datetimeformat = "%Y-%m-%d %H:%M:%S"
    epoch = datetime.datetime.strptime("1980-01-06 00:00:00",datetimeformat)
    elapsed = datetime.timedelta(days=(gpsweek*7),seconds=(gpsseconds))
    return epoch + elapsed

def dec_to_dt(dec):
    """Return the conversion of a a decimal year to datetime"""
    year = int(dec)
    rem = dec - year
    base = datetime.datetime(year, 1, 1)
    date = base + datetime.timedelta(seconds=(base.replace(year=base.year + 1) - base).total_seconds() * rem)
    return date

def dt_to_dec(dt):
    """Return the conversion of a datetime to decimal year"""
    year_start = datetime.datetime(dt.year, 1, 1)
    year_end = year_start.replace(year=dt.year+1)
    return dt.year + ((dt - year_start).total_seconds() /  # seconds so far
        float((year_end - year_start).total_seconds()))  # seconds in year

def ConcatenationLoop(fileList):
    """
    Return a concatenated string of all the contents of the files in the fileList
    """
    outString = ""
    for file in fileList:
        inputFile = open(file,'r')
        outString += inputFile.read()
        inputFile.close()
    return outString


def ConvertGKA_to_ReadableInformation(text):
    """
    Argument:
    - text a string of the contents of a gka file
    Return:
    - A string containing a gka like structure with corrected position and decimal years for each prism 
    """
    outString = ""

    ele = ""
    i=0
    count=0
    for e in text:
        if e!=',' and e!='\n':
            ele+=e

        else: #When ele is complete
            if ele!="":
                 param[i] = ele
            else:
                param[i] = "9999"
               

            i+=1
            if e=='\n':
                if i==32:
                    #Prism
                    for k in range(i):
                        prismParam[k][1] = param[k]
                    
                    GPSwk = int(FindValueByName("GPSwk",prismParam))
                    SOWk = float(FindValueByName("SOWk",prismParam))
                    DOWk = float(FindValueByName("DOWk",prismParam))
                    decYear = dt_to_dec(gps_to_dt(GPSwk, SOWk))

                    DI = float(FindValueByName("DI",prismParam))
                    Beta = float(FindValueByName("Beta",prismParam)) #Rotation around the horizontal axis
                    Alpha = float(FindValueByName("Alpha",prismParam)) #Rotation around the vertical axis

                    ref = 0.0

                    if DI!=0:

                        Gis =  (V0 + Alpha - ref)*PI/200 # in radiants
                        Horizon = Beta*PI/200 # in radiants

                        originXrot = math.sin(Horizon) * math.sin(Gis)
                        originYrot = math.sin(Horizon) * math.cos(Gis)
                        originZrot = math.cos(Horizon)

                        #Position without correction
                        xi = XS + DI * originXrot
                        yi = XS + DI * originYrot
                        zi = XS + DI * originZrot

                        Pression = float(FindValueByName("Pression",prismParam))
                        Temp = float(FindValueByName("Temp",prismParam))
                        
                        #Position with meteorological correction
                        Dmeteo = DI + DI * (COEFF_J - COEFF_N * Pression / (273.16+Temp)) * math.pow(10,-6)
                        xmeteo = XS + originXrot * Dmeteo
                        ymeteo = XS + originYrot * Dmeteo
                        zmeteo = XS + originZrot * Dmeteo
                        
                        #outString
                        outString += FindValueByName("prisme", prismParam) + ','
                        outString += FindValueByName("Pos", prismParam) + ','
                        outString += str(xi) + ','
                        outString += str(yi) + ','
                        outString += str(zi) + ','
                        outString += str(xmeteo) + ','
                        outString += str(ymeteo) + ','
                        outString += str(zmeteo) + ','
                        outString += str(decYear) + ','
                        outString += str(GPSwk) + ','
                        outString += str(DOWk) + ','
                        outString += str(SOWk) + '\n'

                    else:# DI is equal to 0
                        #outString
                        outString += FindValueByName("prisme", prismParam) + ','
                        outString += FindValueByName("Pos", prismParam) + ','
                        outString += "0,0,0,0,0,0,"
                        outString += str(decYear) + ','
                        outString += str(GPSwk) + ','
                        outString += str(DOWk) + ','
                        outString += str(SOWk) + '\n'

                elif i==1:
                    #Start or End of a set
                    if (param[0]=="#GNV11"):
                        count+=1
                        outString+= "#GNV11\n"
                    else:
                        outString+= "#END11\n"

                elif i==15:
                    pass

                i=0
            ele=""
            
    return outString

def From_ReadableInformation_to_list(text):
    #text must be a converted GKA file
    outData = [] #[[Name,[Data]],[],[],...]

    ele = ""
    i=0 #parameter counter
    count=0 #data batch counter
    for e in text:
        if e!=',' and e!='\n':
            ele+=e

        else: #When ele is complete
            if ele!="":
                param[i] = ele
            else:
                param[i] = "9999"

            i+=1
            if e=='\n':
                if i==12:
                    #Prism  >> (0)pos (1)xi (2)yi (3)zi (4)xmeteo (5)ymeteo (6)zmeteo (7)decimalYear (8)GPSwk (9)DOWk (10)SOWk
                    dataList = [] #Pos xi yi zi xmeteo ymeteo zmeteo Week Day Seconds decimalYear
                    for k in range(1,12):
                        dataList.append(float(param[k]))
                    dataList
                    prismIndex = FindIndexByName(param[0], outData) #find the index of the prism withe the name param[0]
                    if prismIndex == None:
                        outData.append([param[0], [dataList]]) #if there is no element in the list for the current prism create an element
                    else:
                        outData[prismIndex][1].append(dataList)

                elif i==1:
                    #Start or End of a set
                    if (param[0]=="#GNV11"):
                        pass
                    else:
                        count+=1
                else:
                    print("Wrong File Format! (need convertedGKA string)")

                i=0
            ele = ""
    return outData