# reverse_complement.py
# Reads a DNA sequence from a FASTA file and prints its
# reverse complement.

COMPLEMENT = {"A": "T", "T": "A", "C": "G", "G": "C"}

def read_fasta_sequence(path):
    """Return the sequence from a single-record FASTA file."""
    sequence = []
    found_header = False
    with open(path) as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if found_header:
                    raise ValueError("FASTA file must contain exactly one record")
                found_header = True
                continue
            if not found_header:
                raise ValueError(
                    f"Expected a FASTA header before sequence on line {line_number}"
                )
            sequence.append(line)

    if not found_header:
        raise ValueError("FASTA file must contain a record header")
    if not sequence:
        raise ValueError("FASTA record contains no sequence")
    return "".join(sequence)

def reverse_complement(seq):
    """Return the reverse complement of a DNA sequence."""
    try:
        return "".join(COMPLEMENT[base] for base in reversed(seq))
    except KeyError as error:
        raise ValueError(
            f"Invalid DNA character {error.args[0]!r}; sequence must contain only A, T, C, and G"
        ) from error

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Print the reverse complement of a single-record FASTA file."
    )
    parser.add_argument("fasta_file", help="path to the FASTA file")
    args = parser.parse_args()
    seq = read_fasta_sequence(args.fasta_file)
    print(reverse_complement(seq)) 
