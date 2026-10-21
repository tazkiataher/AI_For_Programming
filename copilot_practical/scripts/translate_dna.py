
from Bio.Seq import Seq

def translate(seq):
    protein = Seq(seq).translate(to_stop=True)
    return str(protein)

dna = "ATGGCCATTGTAATGGGC"
print(translate(dna))
 


