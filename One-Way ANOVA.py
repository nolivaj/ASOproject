# Comparing diffrent lengths of the hairpin

# One-way ANOVA statistical test in multiple datasets

import scipy.stats as stats

# Datasets in use for the statistical analysis
dataset1_FE = []
dataset2_FE = []
dataset3_FE = []
dataset4_FE = []

dataset1_EP = []
dataset2_EP = []
dataset3_EP = []
dataset4_EP = []

#For each sequence the text files used for the analysis were changed manually
# For example: for sequence_1 to retrieve the data of the file with hairpin lenght 4 the code used was: 
# with open('data_seq1_5.txt', 'r') as file:
#    for line in file:
#        values = line.strip().split(' ')  
#        dataset1_FE.append([float(values[3])])
#        dataset1_EP.append([float(values[5])])

# And to retrieve the data for sequence_5 hairpin and hairpin lenght lenght 6 the code used was:
# with open('data_seq5_6.txt', 'r') as file:
#    for line in file:
#        values = line.strip().split(' ')  
#        dataset3_FE.append([float(values[3])])
#        dataset3_EP.append([float(values[5])])

with open('data_seq6_4.txt', 'r') as file:
    for line in file:
        values = line.strip().split(' ')  # Split the code by the spacebar between the data
        dataset1_FE.append([float(values[3])]) # in position 3 is the Free energy value for each sequence
        dataset1_EP.append([float(values[5])]) # in position 5 is the Equilibrium probability value for each sequence
         

with open('data_seq6_5.txt', 'r') as file:
    for line in file:
        values = line.strip().split(' ')  
        dataset2_FE.append([float(values[3])])
        dataset2_EP.append([float(values[5])])

        
with open('data_seq6_6.txt', 'r') as file:
    for line in file:
        values = line.strip().split(' ') 
        dataset3_FE.append([float(values[3])])
        dataset3_EP.append([float(values[5])])

            
with open('data_seq6_7.txt', 'r') as file:
    for line in file:
        values = line.strip().split(' ')  
        dataset4_FE.append([float(values[3])])
        dataset4_EP.append([float(values[5])])


# Perform one-way ANOVA test
f_statistic_FE, p_value_FE = stats.f_oneway(dataset1_FE, dataset2_FE, dataset3_FE, dataset4_FE)
f_statistic_EP, p_value_EP = stats.f_oneway(dataset1_EP, dataset2_EP, dataset3_EP, dataset4_EP)

# Print the results
print("Free energy")
print("F-Statistic:", f_statistic_FE)
print("P-Value:", p_value_FE)

print("Equilibrium probability")
print("F-Statistic:", f_statistic_EP)
print("P-Value:", p_value_EP)
