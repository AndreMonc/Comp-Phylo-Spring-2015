# Sequence Manipulation Exercise
# Code written by Andre Moncrieff with help from Python for Biologists, chapter 8, for translation portion

# Define DNA sequence
dna_sequence = "aaaagctatcgggcccataccccaaacatgttggttaaaccccttcctttgctaattaatccttacgctatctccatcattatctccagcttagccctgggaactattactaccctatcaagctaccattgaatgttagcctgaatcggccttgaaattaacactctagcaattattcctctaataactaaaacacctcaccctcgagcaattgaagccgcaactaaatacttcttaacacaagcagcagcatctgccttaattctatttgcaagcacaatgaatgcttgactactaggagaatgagccattaatacccacattagttatattccatctatcctcctctccatcgccctagcgataaaactgggaattgccccctttcacttctgacttcctgaagtcctacaaggattaaccttacaaaccgggttaatcttatcaacatgacaaaaaatcgccccaatagttttacttattcaactatcccaatctgtagaccttaatctaatattattcctcggcttactttctacagttattggcggatgaggaggtattaaccaaacccaaattcgtaaagtcctagcattttcatcaatcgcccacctaggctg"

# Print DNA sequence (I've printed a few extra things for completeness)
print("DNA sequence: " + dna_sequence.upper())

# Define length of DNA sequence
length_dna_sequence = len(dna_sequence)

# Print length of DNA sequence
print("Length of DNA sequence: " + str(length_dna_sequence))

# Define equivalent RNA sequence
equivalent_rna_sequence = dna_sequence.replace("t","u")

# Print equivalent RNA sequence
print("Equivalent RNA sequence: " + equivalent_rna_sequence.upper())

# Define reverse of DNA sequence
reverse_DNA_sequence = dna_sequence[::-1]

# Create the complement of this reversed DNA sequence 
# This takes four steps
reverse_DNA_sequence_step1 = reverse_DNA_sequence.replace('a','T')
reverse_DNA_sequence_step2 = reverse_DNA_sequence_step1.replace('t','A')
reverse_DNA_sequence_step3 = reverse_DNA_sequence_step2.replace('g','C')
reverse_DNA_sequence_step4 = reverse_DNA_sequence_step3.replace('c','G')

# Make reverse compliment DNA sequence equivalent with step4 variable above
# This step is not necessary but it's nice to work with a more intelligible variable
reverse_compliment_DNA_sequence = reverse_DNA_sequence_step4

# Print reverse compliment DNA sequence
print("Reverse compliment DNA sequence: " + reverse_compliment_DNA_sequence)

# Extract 13th and 14th codons from original DNA sequence
# Each codon is 3 nucleotides long
# First codon starts at nucleotide 1 
# Second codon starts at nucleotide 4
# Third codon starts at nuceleotide 7 and so on. 
# Following from above, the equation for finding starting nucleotide of codon: 
# Starting nucleotide of codon = codon number + 2(codon number - 1)
# Thus, starting nucleotide of codon 13 = 13 + 2(13-1) = nucleotide 37
# First codon ends at nucleotide 3
# Second codon ends at nucleotide 6
# Third codon ends at nucleotide 9 and so on.
# Following from above, the equation for finding ending nucleotide of codon:
# Ending nucleotide of codon = codon number + 2(codon number)
# Thus, ending nucleotide of codon 14 = 14 + 2(14) = nucleotide 42
# Nucleotides 37 and 42 correspond to positions 36 and 41, respectively.
# Thus, to extract positions 36 through 41 the following notation is necessary:
# [36:42]
# Note that the 36 is inclusive and the 42 is exclusive.
codons_13_and_14 = dna_sequence[36:42]
print("Codons 13 and 14: " + codons_13_and_14.upper())

# Translate DNA sequence to amino acids
# Using Vertebrate Mitochondrial Code to skip intermediate transcription step
# Translation table below from Python for Biologist textbook, chapter 8
# I had to make some modifications to the table so that AA outputs 
# matched those given in the Vertebrate Mitochondrial Code.
translation_table = {
    'ATA':'M', 'ATC':'I', 'ATT':'I', 'ATG':'M',
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
    'AGC':'S', 'AGT':'S', 'AGA':'*', 'AGG':'*',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'*', 'TAG':'*',
    'TGC':'C', 'TGT':'C', 'TGA':'W', 'TGG':'W'}

# Trim last two nucleotides off DNA sequence 
# (This gives a complete final codon after translation)
trimmed_dna_sequence = "aaaagctatcgggcccataccccaaacatgttggttaaaccccttcctttgctaattaatccttacgctatctccatcattatctccagcttagccctgggaactattactaccctatcaagctaccattgaatgttagcctgaatcggccttgaaattaacactctagcaattattcctctaataactaaaacacctcaccctcgagcaattgaagccgcaactaaatacttcttaacacaagcagcagcatctgccttaattctatttgcaagcacaatgaatgcttgactactaggagaatgagccattaatacccacattagttatattccatctatcctcctctccatcgccctagcgataaaactgggaattgccccctttcacttctgacttcctgaagtcctacaaggattaaccttacaaaccgggttaatcttatcaacatgacaaaaaatcgccccaatagttttacttattcaactatcccaatctgtagaccttaatctaatattattcctcggcttactttctacagttattggcggatgaggaggtattaaccaaacccaaattcgtaaagtcctagcattttcatcaatcgcccacctaggc"
Length_trimmed_dna_sequence = len(trimmed_dna_sequence)
print("Length of trimmed dna sequence: " + str(Length_trimmed_dna_sequence))

# Here I create a function that takes dna as input and then outputs (or returns) a protein sequence
def translate_dna(dna):
# The protein sequence variable will, not suprisingly, hold the protein sequence 
# notice, however, that a few lines down the protein sequence gets aa added to it
# This process continues until all aa have been added to the protein    
    protein = ""
# Using range function to generate sequence of numbers
# These numbers will correspond to codons
# In the 3-part range argument: 
# 0 refers to starting position 
# 619 refers to non-inclusive ending position 
# 3 refers to step size  
    for start in range(0,618,3):
# This part of the code defines a codon as a three nucleotide piece of DNA        
        codon = dna[start:start+3]
# Here I do the actual retrieval of the aa that corresponds to a codon
        aa = translation_table.get(codon)
# Here the protein gets the appropriate aa (or amino acid) added to it       
        protein = protein + aa
# Final product   
    return protein
# Now, using my new translate function, I will print the translation of the trimmed DNA sequence
print(translate_dna("AAAAGCTATCGGGCCCATACCCCAAACATGTTGGTTAAACCCCTTCCTTTGCTAATTAATCCTTACGCTATCTCCATCATTATCTCCAGCTTAGCCCTGGGAACTATTACTACCCTATCAAGCTACCATTGAATGTTAGCCTGAATCGGCCTTGAAATTAACACTCTAGCAATTATTCCTCTAATAACTAAAACACCTCACCCTCGAGCAATTGAAGCCGCAACTAAATACTTCTTAACACAAGCAGCAGCATCTGCCTTAATTCTATTTGCAAGCACAATGAATGCTTGACTACTAGGAGAATGAGCCATTAATACCCACATTAGTTATATTCCATCTATCCTCCTCTCCATCGCCCTAGCGATAAAACTGGGAATTGCCCCCTTTCACTTCTGACTTCCTGAAGTCCTACAAGGATTAACCTTACAAACCGGGTTAATCTTATCAACATGACAAAAAATCGCCCCAATAGTTTTACTTATTCAACTATCCCAATCTGTAGACCTTAATCTAATATTATTCCTCGGCTTACTTTCTACAGTTATTGGCGGATGAGGAGGTATTAACCAAACCCAAATTCGTAAAGTCCTAGCATTTTCATCAATCGCCCACCTAGGC"))


# The end. Thanks for any comments!
# If I were to do this coding again, I would probably try creating shorter
# but still informative variables
 
