### info ###
"""
Python program : readGKA
(import tree: readGKA <- functions.py <- parameters.py)
Dev start : 03/06/2020
Dev end : /

Goals:
- Read a .gka file
- Differenciate between different line types and elements
- Correct lack of data such as ",," -> ",9999,"
- Write and manipulate data from a gka file and create statistics
- Concatenate n files

Suggestion:
- Ajouter la possibilité de chercher des fichiers avec des wildcards (avec import glob)
"""
#Commentaire: le fichier gka.201911 contient des irrégularités, ex ligne 11796 il n'y a pas de #END11 + la sonde "C013" (ligne 11795) n'a qu'une seule ligne (pos 1 mais pas de pos 2)

### included libraries ###
from functions import * #import the functions.py file

### Execution ###
running = True
while running:
    #Command line interface
    choice = input("\t- '1' : Concatenate n files\n\t- '2' : Prism statistics\n\t- '3' : Plot prism\n\t- '0' or 'q' : Quit\n\nAnswer: ")
    
    if choice == '1':
        fileList = [] # paht list of the files to concatenate
        outFilePath = input("Enter output file : ") #file that will contain the concatenation of all files
        fileName = input("Enter file to concatenate : ") #first file to concatenate
        
        while (fileName!=' ' and fileName!=''): #while the user enters file names
            fileList.append(fileName)
            fileName = input("Enter file to concatenate (otherwise press enter): ")
        
        start_time = time.time() #Get start time
        print("\n--- Operation start ---")
        
        outputFile = open(outFilePath,'w')
        outputFile.truncate() #Empty file

        concatenatedString = ConcatenationLoop(fileList) #get a concatenated string of the files contained in the file list

        outputFile.write(concatenatedString) #Write the concatenated string to the output file
        outputFile.close() # Close the output file

        print("--- The operation executed correctly ---")
        print("--- It took : %s seconds ---\n" % (time.time() - start_time))

    """
    elif choice == '2':
        start_time = time.time() #Get start time
        print("\n--- Operation start ---")
        ### matplotlib part ### not used for now
        #convertedFileName = input("Enter the converted file containing meteo data : ")
        #arrayData3D = ReadConvertedData3D("out1.gka") # returns a list of 3D lists of floats
        inFile = open("out2.txt",'r')
        text = inFile.read()
        inFile.close()

        data = From_ReadableInformation_to_list(text)

        # sort it by the first element (date)
        prism = data[38][1]

        DateHeightData = []
        for e in prism:
            seconds = e[3]*7*86400 + e[4] * 86400 + e[5]
            DateHeightData.append([seconds,e[2]])

        
        DateHeightData = sorted(DateHeightData)


        #Average two same probes
        DateHeightDataAvrg = []
        former = [0,0]
        for e in DateHeightData:
            if e[1]!=0:
                if e[0] - former[0] < 40:
                    DateHeightDataAvrg.pop() #remove last element

                    ele = (e[1]+former[1])/2

                    DateHeightDataAvrg.append([seconds,ele])
                    former = e
                else:
                    DateHeightDataAvrg.append([e[0],e[1]])
                    former = e
        
        #Sum of horizontal movement
        YArray = [e[1] for e in DateHeightData]
        ""
        former = DateHeightDataAvrg[0][1]
        mov = 0
        for e in DateHeightDataAvrg:
            if e[1]!=0:
                mov += e[1]-former
                YArray.append(mov)
                
                former = e[1]
            else:
                YArray.append(0)
        
        #even out mesurements
        ""
        XArray = [e[0] for e in DateHeightData]
        
        #GPSwk + DOWK/7
        #x = np.arange(len(data))
        x = np.array(XArray)
        y = np.array(YArray)

        plotWidget = pg.plot(title="Position des prismes sur le plan horizontal")
        plotWidget.setLabel('left', "z", units='m')
        plotWidget.setLabel('bottom', "x", units='s')
        plotWidget.plot(x, y, pen=None, symbol='o')  ## setting pen=(i,3) automaticaly creates three different-colored pens
        

        
        ""
        ### matplotlib part ### not used for now
        fig, axs = plt.subplots(1,0,constrained_layout=True)
        axs[0,0].set_title("title1")
        axs[0,0].plot(x, y)
        axs[0,1].set_title("title2")
        axs[0,1].plot([1,2,3,4,5,6], [1,2,3,4,5,6])
        axs[1,0].set_title("title3")
        axs[1,0].plot([1,2,3,4,5,6], [1,2,3,4,5,6])
        axs[1,1].set_title("title4")
        axs[1,1].plot([1,2,3,4,5,6], [1,2,3,4,5,6])
        plt.show()
        ""

        ""
        ## build a QApplication before building other widgets
        pg.mkQApp()

        ## make a widget for displaying 3D objects
        view = gl.GLViewWidget()
        view.setBackgroundColor((0, 0, 0))
        view.show()

        ## create three grids, add each to the view
        xgrid = gl.GLGridItem()
        ygrid = gl.GLGridItem()
        zgrid = gl.GLGridItem()

        view.addItem(xgrid)
        view.addItem(ygrid)
        view.addItem(zgrid)
        
        for e in YArray:
            loc=np.array([e[0],e[1],e[2]])
            dot = gl.GLScatterPlotItem(pos=loc, size=3, color=(1.0,1.0,1.0,1.0), pxMode=True)
            dot.setGLOptions('translucent')
            view.addItem(dot)

        ## rotate x and y grids to face the correct direction
        xgrid.rotate(90, 0, 1, 0)
        ygrid.rotate(90, 1, 0, 0)

        ## scale each grid differently
        xgrid.scale(2000.0, 2000.0, 2000.0)
        ygrid.scale(2000.0, 2000.0, 2000.0)
        zgrid.scale(2000.0, 2000.0, 2000.0)
        ""

        print("--- The operation executed correctly ---")
        print("--- It took : %s seconds ---\n" % (time.time() - start_time))
    elif choice == 't':
        start_time = time.time() #Get start time
        print("--- Test start ---")

        inFile = open("gka.201911",'r')
        text = inFile.read()
        inFile.close()

        
        print("--- The test executed correctly ---")
        print("--- It took : %s seconds ---\n" % (time.time() - start_time))
    """

    if choice == '2':
        answer1 = input("Enter gka file (wildcards allowed): ")
        answer2 = input("Enter output file : ")

        start_time = time.time() #Get start time
        print("\n--- Operation start ---")

        inFilePath = glob.glob(answer1) #wildcard search

        text = ""
        for Path in inFilePath: #Concatenate the content of all the files
            inFile = open(Path)
            text += inFile.read()
            inFile.close()

        outFile = open(answer2,'w') #first file we want to write to
        # Erase file contents
        outFile.truncate()


        PrismInfoList = ConvertGKA_to_List(text)
        sortedByPrismAndDate = Sort_list_by_Prism_and_Date(PrismInfoList)

        outString = ""
        prismInfo = [] # [[prism, nbFound/nbObs]] a 2D list
        for j in sortedByPrismAndDate:
            nbObs = 0
            nbObsPos1 = 0
            nbObsPos2 = 0
            nbFound = 0
            nbFoundPos1 = 0
            nbFoundPos2 = 0

            

            for d in j[1]:
                nbObs += 1;
                if d[1] == 1:
                    nbObsPos1+=1
                    if (d[6]+d[7]+d[8])!=0:
                        nbFoundPos1 += 1
                else:
                    if (d[6]+d[7]+d[8])!=0:
                        nbFoundPos2 += 1
            
            nbObsPos2 = nbObs - nbObsPos1
            nbFound = nbFoundPos1 + nbFoundPos2
            dateStart = dec_to_dt(sortedByPrismAndDate[0][1][0][2]) #Date of the first recording
            dateEnd = dec_to_dt(sortedByPrismAndDate[0][1][-1][2]) #Date of the last recording

            prismInfo.append([j[0], nbFound/nbObs])
            
            outString += "Prisme [\"{}\"] | Date: {} - {}\n".format(j[0], dateStart, dateEnd)
            outString += "Searches : {}        -> Pos1: {}        | Pos2: {}\n".format(nbObs, nbObsPos1, nbObsPos2)
            if nbObs != 0:
                outString += "Found    : {} or {}% -> Pos1: {} or {}% | Pos2: {} or {}%\n".format(nbFound, (nbFound/nbObs)*100, nbFoundPos1, (nbFoundPos1/nbObs)*100*(nbObs/nbObsPos1), nbFoundPos2, (nbFoundPos2/nbObs)*100*(nbObs/nbObsPos2))
            outString += '\n'
        

        prismInfo = SortCrescent(prismInfo, 1) # sort by least to most found prism
        prismCrescentString = ""
        prismCrescentString += "List of "+str(len(prismInfo))+" prisms by found amount (in %):\n"
        for g in prismInfo:
            prismCrescentString += "\t -- {} - found {}% of time.\n".format(g[0], g[1]*100)
            
        outString = prismCrescentString + "\n\nRaw Statistics:\n\n"+ outString

        #Write the output strings to the files
        outFile.write(outString)
        # Close the files
        outFile.close()
        

        print("--- The operation executed correctly ---")
        print("--- It took : %s seconds ---\n" % (time.time() - start_time))

    elif choice == '3':

        answer = input("Enter gka file (wildcards allowed): ")
        prismName = input("EnterPrismName: ")
        inFilePath = glob.glob(answer) #Using wildcards

        start_time = time.time() #Get start time
        print("\n--- Operation start ---")

        text = ""

        for Path in inFilePath: #Concatenate the content of all the files
            inFile = open(Path)
            text += inFile.read()
            inFile.close()


        PrismInfoList = ConvertGKA_to_List(text)
        sortedByPrismAndDate = Sort_list_by_Prism_and_Date(PrismInfoList)

        # Create figure
        fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1)
        size = 1.5
        opac = 0.7

        for j in sortedByPrismAndDate:
            if j[0] == prismName:
                
                #Remove all incorrect prism recordings
                filteredList = []
                for g in j[1]:
                    if g[6]+g[7]+g[8] != 0:
                        filteredList.append(g)
                
                datePos1 = []
                datePos2 = []
                eastPos1 = []
                eastMinPosI = FindMin(filteredList, 6)
                eastPos2 = []
                northPos1 = []
                northMinPosI = FindMin(filteredList, 7)
                northPos2 = []
                altPos1 = []
                altMinPosI = FindMin(filteredList, 8)
                altPos2 = []

                print()

                for d in filteredList:
                        if d[1]==1:
                            datePos1.append(dec_to_dt(d[2])) #dec_to_dt(d[7]).strftime("%m/%d/%Y , %H:%M:%S") 
                            eastPos1.append(d[6]-eastMinPosI)
                            northPos1.append(d[7]-northMinPosI)
                            altPos1.append(d[8]-altMinPosI)
                        else:
                            datePos2.append(dec_to_dt(d[2])) #dec_to_dt(d[7]).strftime("%m/%d/%Y , %H:%M:%S") 
                            eastPos2.append(d[6]-eastMinPosI)
                            northPos2.append(d[7]-northMinPosI)
                            altPos2.append(d[8]-altMinPosI)
                            
                myFmt = mdates.DateFormatter('%d-%m-%Y')

                # log y axis
                ax1.xaxis.set_major_formatter(myFmt)
                ax1.plot(datePos1, eastPos1, label=j[0]+'-Pos1', marker='o', ms=size, alpha=opac, markerfacecolor='None', linestyle = 'None')
                ax1.legend()
                ax1.set_xlabel('Date [d-m-Y]')
                ax1.set_ylabel('East pos [m]')
                ax1.set(title='East pos/Date')
                ax1.xaxis.set_major_locator(plt.MaxNLocator(10))
                ax1.yaxis.set_major_locator(plt.MaxNLocator(10))

                # log x axis
                ax2.xaxis.set_major_formatter(myFmt)
                ax2.plot(datePos1, northPos1, label=j[0]+'-Pos1', marker='o', ms=size, alpha=opac, markerfacecolor='None', linestyle = 'None')
                ax2.legend()
                ax2.set_xlabel('Date [d-m-Y]')
                ax2.set_ylabel('North pos [m]')
                ax2.set(title='North pos/Date')
                ax2.xaxis.set_major_locator(plt.MaxNLocator(10))
                ax2.yaxis.set_major_locator(plt.MaxNLocator(10))

                # log x and y axis
                ax3.xaxis.set_major_formatter(myFmt)
                ax3.plot(datePos1, altPos1, label=j[0]+'-Pos1', marker='o', ms=size, alpha=opac, markerfacecolor='None', linestyle = 'None')
                ax3.legend()
                ax3.set_xlabel('Date [d-m-Y]')
                ax3.set_ylabel('Altitude [m]')
                ax3.set(title='Altitude/Date')
                ax3.xaxis.set_major_locator(plt.MaxNLocator(10))
                ax3.yaxis.set_major_locator(plt.MaxNLocator(10))
                


                # log y axis
                ax1.xaxis.set_major_formatter(myFmt)
                ax1.plot(datePos2, eastPos2, label=j[0]+'-Pos2', marker='o', ms=size, alpha=opac, markerfacecolor='None', linestyle = 'None')
                ax1.legend()
                ax1.set_xlabel('Date [d-m-Y]')
                ax1.set_ylabel('East pos [m]')
                ax1.set(title='East pos/Date')
                ax1.xaxis.set_major_locator(plt.MaxNLocator(10))
                ax1.yaxis.set_major_locator(plt.MaxNLocator(10))

                # log x axis
                ax2.xaxis.set_major_formatter(myFmt)
                ax2.plot(datePos2, northPos2, label=j[0]+'-Pos2', marker='o', ms=size, alpha=opac, markerfacecolor='None', linestyle = 'None')
                ax2.legend()
                ax2.set_xlabel('Date [d-m-Y]')
                ax2.set_ylabel('North pos [m]')
                ax2.set(title='North pos/Date')
                ax2.xaxis.set_major_locator(plt.MaxNLocator(10))
                ax2.yaxis.set_major_locator(plt.MaxNLocator(10))

                # log x and y axis
                ax3.xaxis.set_major_formatter(myFmt)
                ax3.plot(datePos2, altPos2, label=j[0]+'-Pos2', marker='o', ms=size, alpha=opac, markerfacecolor='None', linestyle = 'None')
                ax3.legend()
                ax3.set_xlabel('Date [d-m-Y]')
                ax3.set_ylabel('Altitude [m]')
                ax3.set(title='Altitude/Date')
                ax3.xaxis.set_major_locator(plt.MaxNLocator(10))
                ax3.yaxis.set_major_locator(plt.MaxNLocator(10))

        

        ax1.grid()
        ax2.grid()
        ax3.grid()
        fig.canvas.set_window_title('Prism Ploting')
        fig.tight_layout()

        print("--- The operation executed correctly ---")
        print("--- It took : %s seconds ---\n" % (time.time() - start_time))
        
        plt.show()



    elif choice == '0' or choice == 'q':
        running=False

    else:
        print("\n--- /!\ This option does not exist (%s) ---\n" % choice)


print("--- The program executed correctly ---")

