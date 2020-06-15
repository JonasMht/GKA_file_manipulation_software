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
    <details>
    <summary>Argument</summary>
    
    - **li** a 2D list of floats
    - **index** an integer
    
    </details>
    <details>
    <summary>Return</summary>
    
    - A sorted and crescent list by the elements located at the **index** position of **li**.
    
    </details>
        <br/>
- **FindIndexByName(name, l)**
    <details>
    <summary>Argument</summary>

    - **name** a string
    - **l** the prismParam global list
    
    </details>
    <details>
    <summary>Return</summary>
    
    - The index of the element that contains the correct name in the prismParam list **l**.
    
    </details>
        <br/>
- **FindValueByName(name, l)**
    <details>
    <summary>Argument</summary>

    - **name** a string
    - **l** the prismParam global list
    
    </details>
    <details>
    <summary>Return</summary>
    
    - The value that is linked to the name in the prismParam list **l**.
    
    </details>
        <br/>
- **ChangeValueByName(name, n, l)**
    <details>
    <summary>Argument</summary>

    - **name** a string
    - **n** a float or an integer
    - **l** the prismParam global list
    
    </details>
    <details>
    <summary>Side effect</summary>
    
    - In the prismParam list **l** change the value that is linked to the name to n.
    
    </details>
        <br/>
- **gps_to_dt(gpsweek,gpsseconds)**
    <details>
    <summary>Argument</summary>

    - **gpsweek** an integer
    - **gpsseconds** a float
    
    </details>
    <details>
    <summary>Return</summary>
    
    - Conversion of a GPS date to datetime.
    
    </details>
        <br/>
- **dec_to_dt(dec)**
    <details>
    <summary>Argument</summary>

    - **dec** a float
    
    </details>
    <details>
    <summary>Return</summary>
    
    - Conversion of a decimal year to datetime.
    
    </details>
        <br/>
- **dt_to_dec(dt)**
    <details>
    <summary>Argument</summary>

    - **dt** datetime format
    
    </details>
    <details>
    <summary>Return</summary>
    
    - Conversion of a datetime to decimal year (float).
    
    </details>
        <br/>
- **ConcatenationLoop(fileList)**
    <details>
    <summary>Argument</summary>

    - **fileList** a list of strings
    
    </details>
    <details>
    <summary>Return</summary>
    
    - A concatenated string of all the contents of the files represented by path strings in the fileList/
    
    </details>
        <br/>
- **ConvertGKA_to_ReadableInformation(text)**
    <details>
    <summary>Argument</summary>

    - **text** a string of a gka file.
    
    </details>
    <details>
    <summary>Return</summary>
    
    - A string containing a gka like structure with less elements and corrected position and decimal years for each prism)
    
    </details>
    <details>
    <summary>Math</summary>
    
    - **GPSwk** = `int(FindValueByName("GPSwk",prismParam))`
    - **SOWk** = `float(FindValueByName("SOWk",prismParam))`
    - **DOWk** = `float(FindValueByName("DOWk",prismParam))`
    - **decYear** = `dt_to_dec(gps_to_dt(GPSwk, SOWk))`
    - **DI** = `float(FindValueByName("DI",prismParam))`
    - **Beta** =  `float(FindValueByName("Beta",prismParam))` Rotation around the horizontal axis
    - **Alpha** = `float(FindValueByName("Alpha",prismParam))` Rotation around the vertical axis
    - **ref** =  `0.0`
    - **Gis** =  `(V0 + Alpha - ref)*PI/200` in radiants
    - **Horizon** = `Beta*PI/200` in radiants
    - **Pression** = `float(FindValueByName("Pression",prismParam))`
    - **Temp** = `float(FindValueByName("Temp",prismParam))`
    - **Dmeteo** = DI + DI * (COEFF_J - COEFF_N * Pression / (273.16+Temp)) * math.pow(10,-6)

    - **originXrot** = `math.sin(Horizon) * math.sin(Gis)`
    - **originYrot** = `math.sin(Horizon) * math.cos(Gis)`
    - **originZrot** = `math.cos(Horizon)`

    - **xi** = `XS + DI * originXrot` _Prism position without correction_
    - **yi** = `XS + DI * originYrot` _Prism position without correction_
    - **zi** = `XS + DI * originZrot` _Prism position without correction_

    - **xmeteo** = `XS + originXrot * Dmeteo`
    - **ymeteo** = `XS + originYrot * Dmeteo`
    - **zmeteo** = `XS + originZrot * Dmeteo`
    
    </details>
    <details>
    <summary>Format (text)</summary>
    
    - Start/End of prism aquisition:
        - "#GNV11" / "#END11" (string)
    - Line of one prism:
        - "prisme , Pos , xi , yi , zi , xmeteo , ymeteo , zmeteo , decYear , GPSwk , DOWk , SOWk" (string)
    
    </details>
        
        <br/>
- (to be continued)

