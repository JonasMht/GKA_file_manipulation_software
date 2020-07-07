### info ###
"""
Python program : GKA_FMS
(import tree: GKA_FMS <- functions.py <- parameters.py)
Dev start : 03/06/2020
Dev end : /

Goals:
- Read a .gka file
- Differenciate between different line types and elements
- Correct lack of data such as ",," -> ",9999,"
- Write and manipulate data from a gka file and create statistics
- Concatenate n files
- Use wildcards in the file search systeme
"""
#Commentaire: le fichier gka.201911 contient des irrégularités, ex ligne 11796 il n'y a pas de #END11 + la sonde "C013" (ligne 11795) n'a qu'une seule ligne (pos 1 mais pas de pos 2)

### included libraries ###
from functions import * #import the functions.py file

logo = " ██████╗ ██╗  ██╗ █████╗     ███████╗███╗   ███╗███████╗*\n██╔════╝ ██║ ██╔╝██╔══██╗    ██╔════╝████╗ ████║██╔════╝\n██║  ███╗█████╔╝ ███████║    █████╗  ██╔████╔██║███████╗\n██║   ██║██╔═██╗ ██╔══██║    ██╔══╝  ██║╚██╔╝██║╚════██║\n╚██████╔╝██║  ██╗██║  ██║    ██║     ██║ ╚═╝ ██║███████║\n ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝     ╚═╝     ╚═╝╚══════╝\n\n"

subText = "* File Manipulation Software\n\n\n"

print(logo+subText)

### Execution ###
running = True
while running:
    #Command line interface
    choice = input("\t- '1' : Concatenate n files\n\t- '2' : Prism statistics\n\t- '3' : Plot n given prisms with averaged position\n\t- '4' : Plot n given prisms with Pos1 and Pos2\n\t- '5' : Convert n GKA files to organised text file\n\t- '0' or 'q' : Quit\n\nAnswer: ")
    
    if choice == '1':
        inFilePaths = [] # paht list of the files to concatenate
        fileName = input("Enter a file to concatenate : ") #first file to concatenate
        
        while (fileName!=' ' and fileName!=''): #while the user enters file names
            inFilePath = glob.glob(fileName) #wildcard search
            inFilePaths += inFilePath
            fileName = input("Enter a file to concatenate (otherwise enter nothing): ")
        
        outFilePath = input("Enter output file : ") #file that will contain the concatenation of all files

        start_time = time.time() #Get start time
        print("\n--- Operation start ---")
        
        outputFile = open(outFilePath,'w')
        outputFile.truncate() #Empty file

        text = Convert_FileList_to_String(inFilePaths) #get a concatenated string of the files contained in the file list

        outputFile.write(text) #Write the concatenated string to the output file
        outputFile.close() # Close the output file

        print("--- The operation executed correctly ---")
        print("--- It took : %s seconds ---\n" % int(time.time() - start_time))

    elif choice == '2':

        inFilePaths = [] # paht list of the files to concatenate
        fileName = input("Enter gka file (wildcards allowed): ")

        while (fileName!=' ' and fileName!=''): #while the user enters file names
            inFilePath = glob.glob(fileName) #wildcard search
            inFilePaths += inFilePath
            fileName = input("Enter gka file (otherwise enter nothing): ")

        start_time = time.time() #Get start time
        print("\n--- Operation start ---")

        text = Convert_FileList_to_String(inFilePaths)

        print("\nProcessing...\n")

        PrismInfoList = ConvertGKA_to_List(text)
        sortedByPrismAndDate = Sort_list_by_Prism_and_Date(PrismInfoList)
        
        startDateStr = dec_to_dt(FindMin(sortedByPrismAndDate[0][1], 2)).strftime("%m%d%Y") #Date of the first recording
        endDateStr = dec_to_dt(FindMax(sortedByPrismAndDate[0][1], 2)).strftime("%m%d%Y") #Date of the last recording
        

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

            prismInfo.append([j[0], nbFound/nbObs])

            prismInfo = SortCrescent(prismInfo, 1) # sort by least to most found prism

            prismCrescentString = "Dates : {} to {}\n".format(startDateStr, endDateStr)
            prismCrescentString += "List of "+str(len(prismInfo))+" prisms by found amount (in %):\n"
            for g in prismInfo:
                prismCrescentString += "\t{} {}%\n".format(g[0], int(g[1]*100))

            outString += '\n'
            
            outString += "Prism [\"{}\"] | Date: {} - {}\n".format(j[0],  startDateStr, endDateStr)
            outString += "Searches : {}        -> Pos1: {}        | Pos2: {}\n".format(nbObs, nbObsPos1, nbObsPos2)
            if nbObs != 0:
                outString += "Found    : {} or {}% ".format(nbFound, int((nbFound/nbObs)*100))
                if(nbObsPos1 != 0):
                    outString += "-> Pos1: {} or {}% ".format(nbFoundPos1, int((nbFoundPos1/nbObs)*100*(nbObs/nbObsPos1)))
                if(nbObsPos2 != 0):
                    outString += "| Pos2: {} or {}%".format(nbFoundPos2, int((nbFoundPos2/nbObs)*100*(nbObs/nbObsPos2)))
                outString += '\n'      
            
        outString = prismCrescentString + "\n\nRaw Statistics:\n\n"+ outString


        dates = startDateStr + "_" + endDateStr

        path = "statistics\\" + dates
        pathlib.Path(path).mkdir(parents=True, exist_ok=True) #Create figures directory if it does not exist

        fileName = path + "\\Prism_Statistics_" + dates + ".txt"
        outFile = open(fileName,'w') #first file we want to write to
        # Erase file contents
        outFile.truncate()
        #Write the output strings to the files
        outFile.write(outString)
        # Close the files
        outFile.close()

        print("File saved in .\\" + path + "\n")
        

        print("--- The operation executed correctly ---")
        print("--- It took : %s seconds ---\n" % int(time.time() - start_time))

    elif choice == '3':

        inFilePaths = [] # paht list of the files to concatenate
        fileName = input("Enter gka file (wildcards allowed): ")

        while (fileName!=' ' and fileName!=''): #while the user enters file names
            inFilePath = glob.glob(fileName) #wildcard search
            inFilePaths += inFilePath
            fileName = input("Enter gka file (otherwise enter nothing): ")

        prismList = [] # Prisms that will be shown on the graph
        prismName = input("Enter a prism name (enter nothing for all prisms): ")
        
        while (prismName!=' ' and prismName!=''): #while the user enters prism names
            prismList.append(prismName)
            prismName = input("Enter another prism name (otherwise enter nothing): ")

        start_time = time.time() #Get start time
        print("\n--- Operation start ---")

        text = Convert_FileList_to_String(inFilePaths)

        print("\nProcessing...\n")

        PrismInfoList = ConvertGKA_to_List(text)
        sortedByPrismAndDate = Sort_list_by_Prism_and_Date(PrismInfoList)

        startDateStr = dec_to_dt(FindMin(sortedByPrismAndDate[0][1], 2)).strftime("%m%d%Y") #Date of the first recording
        endDateStr = dec_to_dt(FindMax(sortedByPrismAndDate[0][1], 2)).strftime("%m%d%Y") #Date of the last recording
        
        #eastMax = FindMax( [ e[1] for e in sortedByPrismAndDate], 3)[3]
        #northMax = FindMax( [ e[1] for e in sortedByPrismAndDate], 4)[4]
        #upMax = FindMax( [ e[1] for e in sortedByPrismAndDate], 5)[5]

        # Create figures

        myFmt = mdates.DateFormatter('%d-%m-%Y')

        numRef100 = len(sortedByPrismAndDate[0][1]) #number of ref100 prisms
        adjustment = numRef100/10000

        amountOfPrisms = len(sortedByPrismAndDate)

        plot1 = plt.figure(1)
        plot1.set_size_inches(20 + 20*adjustment, 10 + 20*(1/2)*adjustment) #graph dimensions (inches)
        plot1.suptitle('Time series of position East, using pressure and temperature\nWith '+ str(amountOfPrisms) + " prisms") #plot title
        #plt.ylim(0, 3.5) # setting the ticks
        plt.xticks(rotation=60)
        plt.grid() # use grids

        plot2 = plt.figure(2)
        plot2.set_size_inches(20 + 20*adjustment, 10 + 20*(1/2)*adjustment) #graph dimensions (inches)
        plot2.suptitle('Time series of position North, using pressure and temperature\nWith '+ str(amountOfPrisms) + " prisms")
        #plt.ylim(0, 3.5) # setting the ticks
        plt.xticks(rotation=60)
        plt.grid()
        
        plot3 = plt.figure(3)
        plot3.set_size_inches(20 + 20*adjustment, 10 + 20*(1/2)*adjustment) #graph dimensions (inches)
        plot3.suptitle('Time series of position Up, using pressure and temperature\nWith '+ str(amountOfPrisms) + " prisms")
        #plt.ylim(0, 3.5) # setting the ticks
        plt.xticks(rotation=60)
        plt.grid()

        size = 2 + 0.5+adjustment # size of each dot on the graph
        opac = 0.7 # transparency of each dot

        for j in sortedByPrismAndDate:
            if j[0] in prismList or len(prismList) == 0:
                
                #Remove all incorrect prism recordings
                filteredList = []
                for g in j[1]:
                    if g[6]+g[7]+g[8] != 0:
                        filteredList.append(g)
                

                date = []
                east= []
                eastMin = FindMin(filteredList, 6) # smallest value for east
                north = []
                northMin = FindMin(filteredList, 7) # smallest value for north
                up = []
                upMin = FindMin(filteredList, 8) # smallest value for up

                fistMesurement = [0,0,0,0] # first mesurement of the two positions of a prism
                for d in filteredList:
                        if d[1]==1: # if it is the first prism position
                            fistMesurement[0] = d[2]
                            fistMesurement[1] = d[6]
                            fistMesurement[2] = d[7]
                            fistMesurement[3] = d[8]
                        else:
                            if (fistMesurement[0] == 0 and fistMesurement[1] == 0 and fistMesurement[2] == 0 and fistMesurement[3] == 0):
                                date.append( dec_to_dt(d[2]) )
                                east.append(d[6]- eastMin)
                                north.append(d[7] - northMin)
                                up.append( d[8]- upMin)
                            else:
                                date.append( dec_to_dt( ( d[2] + fistMesurement[0] ) / 2 ) )
                                east.append( ( d[6] + fistMesurement[1] ) / 2 - eastMin)
                                north.append( ( d[7] + fistMesurement[2] ) / 2 - northMin)
                                up.append( ( d[8] + fistMesurement[3] ) / 2 - upMin)
                                fistMesurement = [0,0,0,0]
                            

                # log y axis
                plt.figure(1)
                plt.plot(date, east, label=j[0]+'-AvrgPos', marker='o', ms=size, alpha=opac, markerfacecolor='None', linestyle = 'None')

                plt.legend()
                plt.xlabel('Date (d-m-Y)')
                plt.ylabel('East (m)')

                ax = plt.gca()
                ax.xaxis.set_major_formatter(myFmt)
                ax.xaxis.set_major_locator(plt.MaxNLocator(10))
                ax.yaxis.set_major_locator(plt.MaxNLocator(10))

                plt.figure(2)
                plt.plot(date, north, label=j[0]+'-AvrgPos', marker='o', ms=size, alpha=opac, markerfacecolor='None', linestyle = 'None')

                plt.legend()
                plt.xlabel('Date (d-m-Y)')
                plt.ylabel('North (m)')

                ax = plt.gca()
                ax.xaxis.set_major_formatter(myFmt)
                ax.xaxis.set_major_locator(plt.MaxNLocator(10))
                ax.yaxis.set_major_locator(plt.MaxNLocator(10))


                plt.figure(3)
                plt.plot(date, up, label=j[0]+'-AvrgPos', marker='o', ms=size, alpha=opac, markerfacecolor='None', linestyle = 'None')

                plt.legend()
                plt.xlabel('Date (d-m-Y)')
                plt.ylabel('Up (m)')

                ax = plt.gca()
                ax.xaxis.set_major_formatter(myFmt)
                ax.xaxis.set_major_locator(plt.MaxNLocator(10))
                ax.yaxis.set_major_locator(plt.MaxNLocator(10))


        print("--- The operation executed correctly ---")
        print("--- It took : %s seconds ---\n" % int(time.time() - start_time))

        figAdjustement = adjustment/11

        plt.figure(1)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1),
          fancybox=True, shadow=True, ncol=2)
        plt.subplots_adjust(left=0.05, bottom=0.12, right=.8+figAdjustement, top=.9, wspace=None, hspace=None)
          
        plt.figure(2)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1),
          fancybox=True, shadow=True, ncol=2)
        plt.subplots_adjust(left=0.05, bottom=0.12, right=.8+figAdjustement, top=.9, wspace=None, hspace=None)

        plt.figure(3)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1),
          fancybox=True, shadow=True, ncol=2)
        plt.subplots_adjust(left=0.05, bottom=0.12, right=.8+figAdjustement, top=.9, wspace=None, hspace=None)

        dates = startDateStr + "_" + endDateStr
        path = "graphs\\" + dates + "_" + str(sorted(prismList)).replace(",","_").replace("\'","").strip("[]")
        pathlib.Path(path).mkdir(parents=True, exist_ok=True) #Create figures directory if it does not exist

        imageName = "Prism_Plot_Avrg_Pos" + dates + ".png"
        
        #Save all figures
        plot1.savefig(path + "\\East_"+imageName, dpi=100)
        plot2.savefig(path + "\\North_"+imageName, dpi=100)
        plot3.savefig(path + "\\Up_"+imageName, dpi=100)

        print("Plots saved in .\\" + path + "\n")

        #Clear all figures
        plot1.clf()
        plot2.clf()
        plot3.clf()


    elif choice == '4':

        inFilePaths = [] # paht list of the files to concatenate
        fileName = input("Enter gka file (wildcards allowed): ")

        while (fileName!=' ' and fileName!=''): #while the user enters file names
            inFilePath = glob.glob(fileName) #wildcard search
            inFilePaths += inFilePath
            fileName = input("Enter gka file (otherwise enter nothing): ")

        prismList = [] # Prisms that will be shown on the graph
        prismName = input("Enter a prism name (enter nothing for all prisms): ")
        
        while (prismName!=' ' and prismName!=''): #while the user enters prism names
            prismList.append(prismName)
            prismName = input("Enter another prism name (otherwise enter nothing): ")

        start_time = time.time() #Get start time
        print("\n--- Operation start ---")

        text = Convert_FileList_to_String(inFilePaths)

        print("\nProcessing...\n")

        PrismInfoList = ConvertGKA_to_List(text)
        sortedByPrismAndDate = Sort_list_by_Prism_and_Date(PrismInfoList)

        startDateStr = dec_to_dt(FindMin(sortedByPrismAndDate[0][1], 2)).strftime("%m%d%Y") #Date of the first recording
        endDateStr = dec_to_dt(FindMax(sortedByPrismAndDate[0][1], 2)).strftime("%m%d%Y") #Date of the last recording

        # Create figures

        myFmt = mdates.DateFormatter('%d-%m-%Y')

        numRef100 = len(sortedByPrismAndDate[0][1]) #number of ref100 prisms
        adjustment = numRef100/10000

        amountOfPrisms = len(sortedByPrismAndDate)

        plot1 = plt.figure(1)
        plot1.set_size_inches(20 + 20*adjustment, 10 + 20*(1/2)*adjustment) #graph dimensions (inches)
        plot1.suptitle('Time series of position East, using pressure and temperature\nWith '+ str(amountOfPrisms) + " prisms") #plot title
        #plt.ylim(0, 3.5) # setting the ticks
        plt.xticks(rotation=60)
        plt.grid() # use grids

        plot2 = plt.figure(2)
        plot2.set_size_inches(20 + 20*adjustment, 10 + 20*(1/2)*adjustment) #graph dimensions (inches)
        plot2.suptitle('Time series of position North, using pressure and temperature\nWith '+ str(amountOfPrisms) + " prisms")
        #plt.ylim(0, 3.5) # setting the ticks
        plt.xticks(rotation=60)
        plt.grid()
        
        plot3 = plt.figure(3)
        plot3.set_size_inches(20 + 20*adjustment, 10 + 20*(1/2)*adjustment) #graph dimensions (inches)
        plot3.suptitle('Time series of position Up, using pressure and temperature\nWith '+ str(amountOfPrisms) + " prisms")
        #plt.ylim(0, 3.5) # setting the ticks
        plt.xticks(rotation=60)
        plt.grid()

        size = 2 + 0.5+adjustment # size of each dot on the graph
        opac = 0.7 # transparency of each dot

        for j in sortedByPrismAndDate:
            if j[0] in prismList or len(prismList) == 0:
                
                #Remove all incorrect prism recordings
                filteredList = []
                for g in j[1]:
                    if g[6]+g[7]+g[8] != 0:
                        filteredList.append(g)
                
                datePos1 = []
                datePos2 = []
                eastPos1 = []
                eastMinPosI = FindMin(filteredList, 6) # smallest value for east
                eastPos2 = []
                northPos1 = []
                northMinPosI = FindMin(filteredList, 7) # smallest value for north
                northPos2 = []
                upPos1 = []
                upMinPosI = FindMin(filteredList, 8) # smallest value for up
                upPos2 = []


                for d in filteredList:
                        if d[1]==1:
                            datePos1.append(dec_to_dt(d[2])) #dec_to_dt(d[7]).strftime("%m/%d/%Y , %H:%M:%S") 
                            eastPos1.append(d[6]-eastMinPosI)
                            northPos1.append(d[7]-northMinPosI)
                            upPos1.append(d[8]-upMinPosI)
                        else:
                            datePos2.append(dec_to_dt(d[2])) #dec_to_dt(d[7]).strftime("%m/%d/%Y , %H:%M:%S") 
                            eastPos2.append(d[6]-eastMinPosI)
                            northPos2.append(d[7]-northMinPosI)
                            upPos2.append(d[8]-upMinPosI)
                            

                # log y axis
                plt.figure(1)
                plt.plot(datePos1, eastPos1, label=j[0]+'-Pos1', marker='o', ms=size, alpha=opac, markerfacecolor='None', linestyle = 'None')
                plt.plot(datePos2, eastPos2, label=j[0]+'-Pos2', marker='o', ms=size, alpha=opac, markerfacecolor='None', linestyle = 'None')

                plt.legend()
                plt.xlabel('Date (d-m-Y)')
                plt.ylabel('East (m)')

                ax = plt.gca()
                ax.xaxis.set_major_formatter(myFmt)
                ax.xaxis.set_major_locator(plt.MaxNLocator(10))
                ax.yaxis.set_major_locator(plt.MaxNLocator(10))

                plt.figure(2)
                plt.plot(datePos1, northPos1, label=j[0]+'-Pos1', marker='o', ms=size, alpha=opac, markerfacecolor='None', linestyle = 'None')
                plt.plot(datePos2, northPos2, label=j[0]+'-Pos2', marker='o', ms=size, alpha=opac, markerfacecolor='None', linestyle = 'None')

                plt.legend()
                plt.xlabel('Date (d-m-Y)')
                plt.ylabel('North (m)')

                ax = plt.gca()
                ax.xaxis.set_major_formatter(myFmt)
                ax.xaxis.set_major_locator(plt.MaxNLocator(10))
                ax.yaxis.set_major_locator(plt.MaxNLocator(10))


                plt.figure(3)
                plt.plot(datePos1, upPos1, label=j[0]+'-Pos1', marker='o', ms=size, alpha=opac, markerfacecolor='None', linestyle = 'None')
                plt.plot(datePos2, upPos2, label=j[0]+'-Pos2', marker='o', ms=size, alpha=opac, markerfacecolor='None', linestyle = 'None')

                plt.legend()
                plt.xlabel('Date (d-m-Y)')
                plt.ylabel('Up (m)')

                ax = plt.gca()
                ax.xaxis.set_major_formatter(myFmt)
                ax.xaxis.set_major_locator(plt.MaxNLocator(10))
                ax.yaxis.set_major_locator(plt.MaxNLocator(10))


        print("--- The operation executed correctly ---")
        print("--- It took : %s seconds ---\n" % int(time.time() - start_time))

        figAdjustement = adjustment/11

        plt.figure(1)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1),
          fancybox=True, shadow=True, ncol=2)
        plt.subplots_adjust(left=0.05, bottom=0.12, right=.8+figAdjustement, top=.9, wspace=None, hspace=None)
          
        plt.figure(2)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1),
          fancybox=True, shadow=True, ncol=2)
        plt.subplots_adjust(left=0.05, bottom=0.12, right=.8+figAdjustement, top=.9, wspace=None, hspace=None)

        plt.figure(3)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1),
          fancybox=True, shadow=True, ncol=2)
        plt.subplots_adjust(left=0.05, bottom=0.12, right=.8+figAdjustement, top=.9, wspace=None, hspace=None)

        dates = startDateStr + "_" + endDateStr
        path = "graphs\\" + dates + "_" + str(sorted(prismList)).replace(",","_").replace("\'","").strip("[]")
        pathlib.Path(path).mkdir(parents=True, exist_ok=True) #Create figures directory if it does not exist

        imageName = "Prism_Plot_Pos1_Pos2" + dates + ".png"
        
        #Save all figures
        plot1.savefig(path + "\\East_"+imageName, dpi=100)
        plot2.savefig(path + "\\North_"+imageName, dpi=100)
        plot3.savefig(path + "\\Up_"+imageName, dpi=100)

        print("Plots saved in .\\" + path + "\n")

        #Clear all figures
        plot1.clf()
        plot2.clf()
        plot3.clf()

    elif choice == '5':

        fileList = [] # paht list of the files to concatenate
        fileName = input("Enter a file to convert : ") #first file to concatenate
        
        while (fileName!=' ' and fileName!=''): #while the user enters file names
            inFilePath = glob.glob(fileName) #wildcard search
            fileList += inFilePath
            fileName = input("Enter a file to convert (otherwise enter nothing): ")
        
        start_time = time.time() #Get start time
        print("\n--- Operation start ---")

        text = ""
        numFiles = len(inFilePath)
        count = 1
        for Path in inFilePath: #Concatenate the content of all the files
            inFile = open(Path)
            text += inFile.read()
            print("%i/%i files loaded." % (count, numFiles))
            count+=1
            inFile.close()

        print("\nProcessing...\n")

        PrismInfoList = ConvertGKA_to_List(text)
        sortedByPrismAndDate = Sort_list_by_Prism_and_Date(PrismInfoList)

        startDateStr = dec_to_dt(FindMin(sortedByPrismAndDate[0][1], 2)).strftime("%m%d%Y") #Date of the first recording
        endDateStr = dec_to_dt(FindMax(sortedByPrismAndDate[0][1], 2)).strftime("%m%d%Y") #Date of the last recording

        dates = startDateStr + "_" + endDateStr

        path = "converted_files\\" + dates
        pathlib.Path(path).mkdir(parents=True, exist_ok=True) #Create figures directory if it does not exist

        fileName = path + "\\Converted_" + dates + ".txt"
        outFile = open(fileName,'w') #file we want to write to

        outFile.write(str(sortedByPrismAndDate)) #Write the concatenated string to the output file
        outFile.close() # Close the output file

        print("\nFormat : [[prism1, [[prism1_at_t0, pos, decYear, x, y, z, xmeteo, ymeteo, zmeteo], [prism1_at_t1, ...], ... ]],[prsim2, [...]], [...] ]\n")

        print("File saved in .\\" + path + "\n")

        print("--- The operation executed correctly ---")
        print("--- It took : %s seconds ---\n" % int(time.time() - start_time))

    elif choice == '0' or choice == 'q':
        running=False

    else:
        print("\n--- /!\ This option does not exist (%s) ---\n" % choice)


print("--- The program executed correctly ---")

