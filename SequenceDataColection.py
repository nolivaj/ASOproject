from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import itertools
# The code above repesents all the packages and functions needed to the development of this code

#Initially, we want to figure out all the possibilities of hairpin sequences (with at least 1 'GC')
# to do this, a series of steps are taken

# Define the nucleotides
nucleotides = ['A', 'C', 'G', 'T']

# Define hairpin length
length = 2 # the length of the hairpin structure was manually changed for each sequence

#Define sequence
Sequence_1 = "AATTCAGGGCGAGGACCATAG" # the sequence present betweeen the hairpin structure (found in literature and
                                    # defined in the report) was changed manualy according to the sequence in analysis


# To develop an hairpin structure (structure in wich the beginning and the end 
# of the nucleotide sequence are complementary to each other), the complementary nucleotides needed to be defined
# the following function developed returns the complementary nucleotide of a nucleotide given
def get_complement(nucleotide):
    complements = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return complements[nucleotide]

# if we consider a nucleotide length of 'n', there are n^4 possible combinations for this sequence
# The following code generates all combinations of nucleotides with the length defines above (line 18)
combinations = itertools.product(nucleotides, repeat=length)


hairpins = []
reverse_complementary_hairpins =[]
seq_complement=''


# Additionally, we need to ensure at least one 'GC' pair is present in the structure
# The following code goes throw all the possible sequences (established beforehand - line 34)
# and selects all of those with at least one 'GC'
for combo in combinations:
    for i in range(len(combo)-1):
        if combo[i:i+2] == ('G', 'C'):
            hairpins.append(''.join(combo[:i]) + 'GC' + ''.join(combo[i+2:]))
            break


# Considering we have a list of all the possible sequences with at least 1 'GC',
# we needed to determine the complementary sequence that would go to the end of the established sequence we have
# so we would have: [randomized nucleotide sequence with at least 1'GC'] + [established sequence(line 21)] + [sequence reverse complementary to the one before the established sequence]

# To achieve this we need to loop through the hairpins and create the reverse complement
for seq in hairpins:
    for nuc in seq:
        seq_complement += get_complement(nuc)

    reverse_complementary_hairpins.append(seq_complement[::-1]) # reverse_complementary_hairpins has the reverse complement of the randomized sequences in the same order as its reverse complement
    seq_complement=''
 
sequences = []

# here we combine the hairpin structure with the established sequence to create all the possibilities we require for data analysis later on
for h in range(len(hairpins)):
    
    sequences.append(hairpins[h] + Sequence_1 + reverse_complementary_hairpins[h])
    

#print(len(hairpins))


#Considering we have all the possibilities we need, the NUPACK software was used to retrieve free energy and equilibrium probability data fr posterior 
# selection of the sequence we need
# To achieve this a series of steps were taken and are described here

#Open Nupack Software
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

time.sleep(3) # this time function was used to avoid the malfunction of this whole process as it is conducted very fast and the website wasn't able to keep up

utilities =driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div[1]/div[1]/a[3]')
driver.execute_script("arguments[0].click();",utilities)

data=[]

#After doing the log in and reaching the page in which we can retrieve the data, a series of options needed to be selection in addition to the input of the nucleotide sequences
#Input information
# this code runs through all the sequences and retrieves the corresponding free energy and equilibrium probability values
for sequence in range(0, len(sequences)):

    time.sleep(1)
    #check DNA
    DNA_Button =driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div[3]/div/form/div[2]/div[1]/div/div/div[2]/div/input')
    driver.execute_script("arguments[0].click();", DNA_Button)

    #input temperature
    Temp_Input =driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div[3]/div/form/div[2]/div[2]/div/input')
    Temp_Input.clear()
    Temp_Input.send_keys("37")

    #Salt concentrations - these we maintain in order to compare results
    open_tab = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div[3]/div/form/div[10]/div[1]/div[1]')
    driver.execute_script("arguments[0].click();",open_tab)
    #time.sleep(5)

    Na_Input = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div[3]/div/form/div[10]/div[1]/div[2]/div/div/div[2]/div[3]/div[1]/input')
    Na_Input.clear()
    Na_Input.send_keys("1")
    #time.sleep(5)
    Mg_Input = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div[3]/div/form/div[10]/div[1]/div[2]/div/div/div[2]/div[3]/div[2]/input')
    Mg_Input.clear()
    Mg_Input.send_keys("0.2")
    #time.sleep(5)


    sequenceInput = driver.find_element(By.XPATH,'//*[@id="mysequence"]')

    #Because of the high sample size with a higher number of hairpin lengths, some errors would occur and clearing the 
    # input space before inputing another sequence helped avoid interruption in running the code
    sequenceInput.clear()
    sequenceInput.send_keys(sequences[sequence])
    #time.sleep(2)

    #check MFE
    MFE_Button = driver.find_element(By.XPATH,'/html/body/div/div/div/div/div/div[3]/div/form/div[3]/div[2]/div[1]/input')
    driver.execute_script("arguments[0].click();", MFE_Button)

    time.sleep(1)
    
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

    # 'data' will have all the possible sequences and the corresponding free energy and equilibrium proability values

    driver.get('https://www.nupack.org/utilities/new')

    time.sleep(2)



driver.close()  
with open("data_seq1_2.txt", "w") as f: # the name of the file saved as was changed manually with every sequence and hairpin length
        for arr in range(0,len(data)):
            f.write(' '.join([str(elem) for elem in data[arr]]))
            f.write('\n')
        

    

