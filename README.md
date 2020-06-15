# GKA_file_manipulation_software
The main file of this Python program (readGKA.py) depends on two other files (functions.py & parameters.py) that both provide useful functions
aswell as global variables and librarie imports.

## Imported libraries:

- **time** (provides a function to get current time in seconds)
- **datetime** (provides date conversion functions)
- **math** (provides math functions)


## Global Variables:

- **XS YS ZS** (position of the total station in meters)
- **V0** (yaw rotation in Gradians)
- **COEFF_J & COEFF_N** (two constants used in the meteorological correction formula provided by the EDM manufacturer)
- **PI** (value of pi provided by the math library)
- **param** (a list of 32 elements that will hold strings (used in several functions such as ConvertGKA_to_ReadableInformation(text)))
- **prismParam** a list of 34 elements (a list of 2D list containing each a string and a value. This list represents the data contained on a prism line in a gka file)


## Functions:

- **SortCrescent(li, index)** ()
    - Argument:
        - **li** a 2D list of floats
        - **index** an integer
    - Return:
        - A sorted and crescent list by the elements located at the index position of li.
        <br/>
- **FindIndexByName(name, l)**
    - Argument:
        - **name** a string
        - **l** the prismParam global list
    - Return:
        - the index of the element that contains the correct name in the prismParam list l.
        <br/>
- **FindValueByName(name, l)**
    - Argument:
        - **name** a string
        - **l** the prismParam global list
    - Return:
        - The value that is linked to the name in the prismParam list l.
        <br/>
- **ChangeValueByName(name, n, l)**
    - Argument:
        - **name** a string
        - **n** a float or an integer
        - **l** the prismParam global list
    - Side effect:
        - In the prismParam list l change the value that is linked to the name to n.
        <br/>
- **gps_to_dt(gpsweek,gpsseconds)**
    - Argument:
        - **gpsweek** an integer
        - **gpsseconds** a float
    - Return:
        - Conversion of a GPS date to datetime.
        <br/>
- **dec_to_dt(dec)**
    - Argument:
        - **dec** a float
    - Return:
        - Conversion of a decimal year to datetime.
        <br/>
- **dt_to_dec(dt)**
    - Argument:
        - **dt** datetime format
    - Return:
        - conversion of a datetime to decimal year (float).
        <br/>
- **ConcatenationLoop(fileList)**
    - Argument:
        - **fileList** a list of strings
    - Return:
        - A concatenated string of all the contents of the files represented by path strings in the fileList/
        <br/>
- **ConvertGKA_to_ReadableInformation(text)**
    - Argument:
        - **text** a string of a gka file.
    - Return:
        - A string containing a gka like structure with corrected position and decimal years for each prism)
        <br/>
- (to be continued)

