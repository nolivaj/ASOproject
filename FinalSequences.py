
FE = []


data=[]
for j in range(1,7):
    for i in range(4,8):

        file_path = 'data_seq'+str(j)+'_'+str(i)+'.txt'
        

        with open(file_path, 'r') as file1:
            for line1 in file1:
                values = line1.strip().split(' ')
                

                if (-20)<float(values[3])<(-5):

                    #  values[0] - represent the considered sequence
                    #  values[3] - represents the corresponding free energy
                    #  values[5] - represents the corresponding equilibrium probability

                    data.append([values[0],float(values[3]),values[5]])


                    #anothe if loop can be added to select the desired equilibrium probability 

# the text file "FinalSequences.txt" will have all the sequences within the parameters we defined
with open("FinalSequences.txt", "w") as f:
    for arr in data:
        f.write(' '.join([str(elem) for elem in arr]))
        f.write('\n')