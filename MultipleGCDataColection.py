
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import itertools


# This code was developed to create a list of sequences with 2 or 3 'GC' content in the hairpin structure
# this will allow us to compare the list on single and multiple 'GC' with the purpose of knowing if its content 
# is statistically important for free energy and equilibrium probability values

# Define the nucleotides
nucleotides = ['A', 'C', 'G', 'T']
reverse_complementary_hairpins =[]
seq_complement=''

#Define sequence - This was changed manually for all sequences
Sequence_1 = "TTCAGGGCGAGGACCATAGAG"

# Define the complement of each nucleotide
def get_complement(nucleotide):
    
    complements = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return complements[nucleotide]

# The length was changed manually for all hairpin lengths
# Generate all possible combinations of nucleotides of length 7 as this is the hairpin length with over 1 possibility with 3 'GC' content
sequences = list(itertools.product(nucleotides, repeat=7))

# Filter for sequences that contain 3 (or 2) 'GC' nucleotides
filtered_sequences = [seq for seq in sequences if ''.join(seq).count('GC') == 3]


# Convert list of tuples to list of strings
list_of_strings = [''.join(t) for t in filtered_sequences]
#print(list_of_strings)

# Get a list of the reverse complemente haipin sequences
for seq in list_of_strings:

    for nuc in seq:
        seq_complement += get_complement(nuc)

    reverse_complementary_hairpins.append(seq_complement[::-1])
    seq_complement=''
 
#print(reverse_complementary_hairpins)
sequences = []


for h in range(len(filtered_sequences)):
    
    sequences.append(list_of_strings[h] + Sequence_1 + reverse_complementary_hairpins[h])
    



#Open Nupack
driver = webdriver.Chrome()

driver.get('https://www.nupack.org/')
time.sleep(2)

#log in the website

log_in =driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div[1]/div[2]/a[2]')
driver.execute_script("arguments[0].click();",log_in)

email =driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div[2]/div/div/form/div[1]/div/div/input')
email.send_keys("marta.moreira@iqs.url.edu")

password =driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div[2]/div/div/form/div[2]/div/div/input')
password.send_keys("marta123456789")

log_in_button=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div[2]/div/div/div/div/div/div/button[2]')
driver.execute_script("arguments[0].click();",log_in_button)

time.sleep(3)

utilities =driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div[1]/div[1]/a[3]')
driver.execute_script("arguments[0].click();",utilities)

data=[]


for sequence in range(0, len(sequences)):

    driver.get('https://www.nupack.org/utilities/new')
    time.sleep(2)
    sequenceInput = driver.find_element(By.XPATH,'//*[@id="mysequence"]')

    sequenceInput.clear()
    sequenceInput.send_keys(sequences[sequence])
    #time.sleep(2)

    #check MFE
    MFE_Button = driver.find_element(By.XPATH,'/html/body/div/div/div/div/div/div[3]/div/form/div[3]/div[2]/div[1]/input')
    driver.execute_script("arguments[0].click();", MFE_Button)

    time.sleep(1)

    #input temperature
    Temp_Input =driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div[3]/div/form/div[2]/div[2]/div/input')
    Temp_Input.clear()
    Temp_Input.send_keys("37")

    #check DNA
    DNA_Button =driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div[3]/div/form/div[2]/div[1]/div/div/div[2]/div/input')
    driver.execute_script("arguments[0].click();", DNA_Button)


    #Salt concentrations
    open_tab = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div[3]/div/form/div[10]/div[1]/div[1]')
    driver.execute_script("arguments[0].click();",open_tab)
    time.sleep(1)

    Na_Input = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div[3]/div/form/div[10]/div[1]/div[2]/div/div/div[2]/div[3]/div[1]/input')
    Na_Input.clear()
    Na_Input.send_keys("1")
    #time.sleep(5)
    Mg_Input = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div[3]/div/form/div[10]/div[1]/div[2]/div/div/div[2]/div[3]/div[2]/input')
    Mg_Input.clear()
    Mg_Input.send_keys("0.2")
    #time.sleep(5)

    
    update = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div[3]/div/form/div[2]/div[3]/button')

    driver.execute_script("arguments[0].click();",update )
    time.sleep(1)

    #Retrieve data
    open_details_tab = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div[3]/div/form/div[9]/div/div[1]/i')
    driver.execute_script("arguments[0].click();",open_details_tab)
    time.sleep(1.5)

    #Free energy
    Free_Energy = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div[3]/div/form/div[9]/div/div[2]/div/div/div[2]/div[1]/table[1]/tbody/tr[3]/td[2]').text

    #Structure Free energy
    Free_Energy_Structure =driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div[3]/div/form/div[9]/div/div[2]/div/div/div[2]/div[2]/table/tbody/tr[1]/td[2]').text

    #Equilibrium probability
    Equilibrium_Probability = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div[3]/div/form/div[9]/div/div[2]/div/div/div[2]/div[2]/table/tbody/tr[2]/td[2]').text
    time.sleep(1)
    data.append([sequences[sequence],Free_Energy,Free_Energy_Structure,Equilibrium_Probability])

    
    time.sleep(1)

   
with open("data3_seq3_7.txt", "w") as f:
    for arr in data:
        f.write(' '.join([str(elem) for elem in arr]))
        f.write('\n')