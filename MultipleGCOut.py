# Remove from list 1 (text file with all the information on the sequences, 
#free energy and equilibrium pribability) the equal sequences in file 2 
#(sequences with multiple 'GC' in the hairpin structure)

def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def write_file(file_path, lines):
    with open(file_path, 'w') as file:
        file.writelines(lines)

def main():
    file1_path = 'data2_seq1_7.txt' # The file path was manually changes for each dataset in use
    file2_path = 'data3_seq1_7.txt'

    file1_lines = read_file(file1_path)
    file2_lines = read_file(file2_path)

    file1_column1 = [line.split()[0] for line in file1_lines]
    file2_column1 = [line.split()[0] for line in file2_lines]

    new_file1_lines = [line for line in file1_lines if line.split()[0] not in file2_column1] #comparison of the data in the 2 files

    write_file(file1_path, new_file1_lines)

    print(len(file1_lines))
    print(len(file2_lines))
    print(len(new_file1_lines))


if __name__ == "__main__":
    main()

# The data repetead in both files will be deleted from the initial file (the file with the seqeunces with all the GC content)
# and saved automatically with the same name    
