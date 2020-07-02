from parameters import * #import the parameters.py file

### Functions ###

def SortCrescent(li, index):
    """
    Argument:
    - li a list of lists.
    - index an integer
    Return:
    - A sorted list of lists in a crescent order by the elements located at the index position of each list contained in li.
    """
    #ex :[
    """"""
    return(sorted(li, key = lambda x: x[index]))

def FindMin(li, index):
    """
    Argument:
    - li a list of lists.
    - index an integer
    Return:
    - Index of the smallest element found in the list at the index position in the li list.
    - If non are found, return 0.
    """
    #ex :[[0,9,8],[1,2,3],[3,4,5]] the min at index 1 is 2
    if (len(li)>0):
        return min([e[index] for e in li])
    return 0

def FindMax(li, index):
    """
    Argument:
    - li a list of lists.
    - index an integer
    Return:
    - Index of the greatest element found in the list at the index position in the li list.
    - If non are found, return 0.
    """
    #ex :[[0,9,8],[1,2,3],[3,4,5]] the min at index 1 is 2
    if (len(li)>0):
        return max([e[index] for e in li])
    return 0


def FindIndexByName(name, l):
    """
    Argument:
    - name a string.
    - l a list.
    Return:
    - Index of the element that contains the correct name found in the prismParam list l.
    """
    pos = 0
    for e in l:
        if e[0]==name:
            return pos
        pos+=1
    return None

def FindValueByName(name, l):
    """
    Argument:
    - name a string.
    - l a list.
    Return:
    - Value that is linked to the name found in the prismParam list l.
    """
    for e in l:
        if e[0]==name:
            return e[1]
    return None

def ChangeValueByName(name, n, l):
    """
    Argument:
    - name a string.
    - n a variable.
    - l a list.
    Side effect:
    - In the prismParam list l change the value that is linked to the name to n.
    """
    for e in l:
        if e[0]==name:
            e[1] = n

def gps_to_dt(gpsweek,gpsseconds):
    """
    Argument:
    - gpsweek an integer.
    - gpsseconds a float.
    Return:
    - Conversion of a GPS date to a date in datetime format.
    """
    datetimeformat = "%Y-%m-%d %H:%M:%S"
    epoch = datetime.datetime.strptime("1980-01-06 00:00:00",datetimeformat)
    elapsed = datetime.timedelta(days=(gpsweek*7),seconds=(gpsseconds))
    return epoch + elapsed

def dec_to_dt(dec):
    """
    Argument:
    - A decimal year.
    Return:
    - Conversion of a a decimal year to a date in datetime format.
    """
    year = int(dec)
    rem = dec - year
    base = datetime.datetime(year, 1, 1)
    date = base + datetime.timedelta(seconds=(base.replace(year=base.year + 1) - base).total_seconds() * rem)
    return date

def dt_to_dec(dt):
    """
    Argument:
    - A date in datetime format.
    Return:
    - Conversion of a datetime to decimal year.
    """
    year_start = datetime.datetime(dt.year, 1, 1)
    year_end = year_start.replace(year=dt.year+1)
    return dt.year + ((dt - year_start).total_seconds() /  # seconds so far
        float((year_end - year_start).total_seconds()))  # seconds in year


def Convert_FileList_to_String(inFilePaths):
    """
    Argument:
    - A list of strings representing file paths.
    Return:
    - A concatenated string of all the contents of the files in the file list.
    """
    text = ""
    numFiles = len(inFilePaths)
    count = 1
    for Path in inFilePaths: #Concatenate the content of all the files
        inFile = open(Path)
        text += inFile.read()
        print("%i/%i files loaded." % (count, numFiles))
        count+=1
        inFile.close()
    return text


def ConvertGKA_to_List(text):
    """
    Argument:
    - text a string of the contents of a gka file.
    Return:
    - A list containing the prism name, position of recording, decimal year, position and meteo corrected position for each prism.
    """
    outList = []

    ele = ""
    i=0
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
                        
                        outList.append([FindValueByName("prisme", prismParam), int(FindValueByName("Pos", prismParam)), decYear, xi, yi, zi, xmeteo, ymeteo, zmeteo])

                    else:# DI is equal to 0
                        outList.append([FindValueByName("prisme", prismParam), int(FindValueByName("Pos", prismParam)), decYear, 0, 0, 0, 0, 0, 0])

                elif i==1:
                    #Start or End of a set
                    pass
                elif i==15:
                    pass

                i=0
            ele=""
            
    return outList

def Sort_list_by_Prism_and_Date(lst):
    """
    Argument:
    - A list containing the prism name, position of recording, decimal year, position and meteo corrected position for each prism.
    Return:
    - A list containing lists of prisms sorted by name and date.
    """
    #text must be a converted GKA file
    outList = [] #[[Name,[Data]],[],[],...]

    #Sort by prism name
    for k in lst:
        index = FindIndexByName(k[0],outList)
        if index != None:
            outList[index][1].append(k)
        else:
            outList.append([k[0],[k]])
    

    #Sort by crescent date
    for j in outList:
        j[1] = SortCrescent(j[1],2)

    return outList