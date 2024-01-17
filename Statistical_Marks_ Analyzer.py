#===========================================================================================================================
#This program is written to analyse marks of students and their rankings in various subjects, from a statsicial perspective.
#Creation Date: 07/05/2020
#Author: Anant Chhabda
#===========================================================================================================================


#This function skips one line of the file
def skipline1(filename): 
    filename.readline()
    return filename.readline()


#This function converts a list of valid strings to a list of integers    
def converttoint(line_list): 
    for i in range(2, len(line_list)):
        line_list[i] = float(line_list[i])
      
      
#This function capitalizes the first element in the list
def capitalize(line_list): #
    line_list[0] = line_list[0].upper()


#This function calculates the standard deviation of a list
def stdv(list):
    sum = 0
    for i in list:
        sum += (i-mean(list))**2
    variance = (sum/len(list))
    std = variance**(1/2)
    return std


#This function calulates the mean of a list
def mean(list):
    Mean = sum(list)/len(list)
    return Mean


#This function returns Spearmans correlation coefficient
def spearcorr(sum,n):
    denom = n*((n**2)-1)
    num = 6*sum
    
    coeff = 1-(num/denom)
    return round(coeff,4)


#This function reads data for each student 
def studentlistcompile(file):
    
    studentfile = open(file, "r")

    line = skipline1(studentfile)
    length = len(line.split(","))
    
    if length>2:
        allstudents = []
        
        #create a list for each line
        while line != "":
            line = line.strip("\n")
            line_list = line.split(",")
            converttoint(line_list)
            capitalize(line_list)
            
            allstudents.append(line_list)
            line = studentfile.readline()
            
        studentfile.close()
        allstudents.sort()
        return allstudents, length

    else:
        print("No Analysis conducted as there have been no marks recorded for students")
        exit()
#This function returns the total marks of each student
def totalmark(allstudents):
    totalmarks = []
    
    #create list of total marks subject wise
    for i in range(len(allstudents)):
        tmark = sum(allstudents[i][2:])
        totalmarks.append(tmark)
    return totalmarks


#This function returns all marks for each subject
def allmark(allstudents,length):
    
    subjectmark = []
    allmarks = []
    
    #create seperate subject mark lists 
    for i in range(2,length):
         
         for j in range(len(allstudents)):
             subjectmark.append(allstudents[j][i])
             
         allmarks.append(subjectmark.copy())
         subjectmark.clear()
         
    return allmarks


#This function does statistical analysis 
def allmarkloop(allmarks,allstudents):
    
    mn = []
    mx = []
    avg = []
    std = []
    ranklist = []
    allranks = []
    
    #sort ranks for each marks list 
    for list in allmarks:
        
        for i in range(len(list)):
            rank = 1 #highest rank start for each mark
            
            for j in range(len(list)):
                if list[i]<list[j]:
                    rank += 1 #add 1 if bigger mark found
                
                if list[i]==list[j] and i!=j and i>j: #rank arrangement if same mark
                   if allstudents[i][0] != allstudents[j][0]:
                        rank+=1
                   else: #errorstate lookout
                        print ("Program has found two students with the same name and same subjectmark/totalmark")
                        exit()
                    
            ranklist.append(rank)
         
        allranks.append(ranklist.copy())
        ranklist.clear()
        
        #building stastistical data
        mn.append(round(min(list),4))
        mx.append(round(max(list),4))
        avg.append(round(mean(list),4))
        std.append(round(stdv(list),4))
        
    return allranks, mn, mx, avg, std

#This function creates a list of all correlations
def corrlist(allranks):
    
    cor = []
    total = 0
    
    #calculating spearman's coefficient
    for list in allranks:
        
        for i in range(len(list)):
            diff = (list[i] - allranks[-1][i])**2
            total+=diff
            
        constant = spearcorr(total,len(list))
        cor.append(constant)
        total = 0
        
    return cor
   

#This function puts it all together and returns lists containing statistical analysis
def main(file):
    
    allstudents, length = studentlistcompile(file)  
    
    totalmarks = totalmark(allstudents)
        
    allmarks = allmark(allstudents, length)
    
    allmarks.append(totalmarks)
           
    allranks, mn, mx, avg, std = allmarkloop(allmarks,allstudents)
        
    cor = corrlist(allranks)
    
    return mn, mx, avg, std, cor