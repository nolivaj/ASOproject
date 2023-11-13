
from scipy.stats import mannwhitneyu # this code imports the function needed to perform the Mann-Whitney U test in the data we have

# The file paths were manually changed to compare the 'GC' content in different hairpin sizes
file1_path = 'data2_seq1_7.txt'
file2_path = 'data3_seq1_7.txt'


# Results - was the match between the 2 files. by using the code to detele the 
# 2 GC and 3 GC solves the problem. change this code
x_values = []
y_values = []

with open(file1_path, 'r') as file1:
    for line1 in file1:
        values = line1.strip().split(' ')
        y_values.append(float(values[3])) # position '3' retrieves Free energy values
        x_values.append(float(values[5])) # position '5' retrieves Equilibrium probability values


#USUALLY FREE ENERGY IS NOT NORMALLY DISTRIBUTED SO MANN WHITCNEY U TEST IS USED
y2_values = []
x2_values = []
with open(file2_path, 'r') as file2:
    for line2 in file2:
        values = line2.strip().split(' ')
        y2_values.append(float(values[3]))
        x2_values.append(float(values[5]))



# Perform Mann-Whitney U test
statistic_FE, p_value_FE = mannwhitneyu(y_values, y2_values)
statistic_EP, p_value_EP = mannwhitneyu(x_values, x2_values)

# Print the results
print("Free energy")
print("Mann-Whitney U statistic:", statistic_FE)
print("P-value:", p_value_FE)

print("Equilibrium probability")
print("Mann-Whitney U statistic:", statistic_EP)
print("P-value:", p_value_EP)
