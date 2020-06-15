# GKA_file_manipulation_software
The main file of this Python program (readGKA.py) depends on two other files (functions.py & parameters.py) that both provide useful functions
aswell as global variables and librarie imports.

## Imported libraries:

- time (provides a function to get current time in seconds)
- datetime (provides date conversion functions)
- math (provides math functions)


## Global Variables:

- **XS YS ZS** (position of the total station in meters)
- **V0** (yaw rotation in Gradians)
- **COEFF_J & COEFF_N** (two constants used in the meteorological correction formula provided by the EDM manufacturer)
- PI (value of pi provided by the math library)
- param (a list of 32 elements that will hold strings (used in several functions such as ConvertGKA_to_ReadableInformation(text)))
- prismParam a list of 34 elements (a list of 2D list containing each a string and a value. This list represents the data contained on a prism line in a gka file)


## Functions:

- SortCrescent(li, index) (Sort a list in a crescent order by the elements located at the index position)
- FindIndexByName(name, l) (In the prismParam list l find and return the index of the element that contains the correct name)
- FindValueByName(name, l) (In the prismParam list l find and return the value that is linked to the name)
- ChangeValueByName(name, n, l) (In the prismParam list l change the value that is linked to the name to n)
- gps_to_dt(gpsweek,gpsseconds) (Return the conversion of a GPS date to datetime)
- dec_to_dt(dec) (Return the conversion of a decimal year to datetime)
- dt_to_dec(dt) (Return the conversion of a datetime to decimal year)
- ConcatenationLoop(fileList) (Return a concatenated string of all the contents of the files represented by path strings in the fileList)
- ConvertGKA_to_ReadableInformation(text)
    - Argument:
        - text a string of the contents of a gka file.
    - Return:
        - A string containing a gka like structure with corrected position and decimal years for each prism)
        - (to be continued)

