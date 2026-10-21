"""Print the GC content of each non-empty FASTA record."""

import argparse
import sys


def read_fasta_records(path):
    """Yield FASTA headers and their concatenated sequences."""
    header = None
    sequence = []

    with open(path) as fasta_file:
        for line_number, line in enumerate(fasta_file, start=1):
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header is not None:
                    yield header, "".join(sequence)
                header = line[1:]
                sequence = []
            else:
                if header is None:
                    raise ValueError(
                        f"Expected a FASTA header before sequence on line {line_number}"
                    )
                sequence.append(line)

    if header is not None:
        yield header, "".join(sequence)


def gc_percentage(sequence):
    """Return the percentage of sequence bases that are G or C."""
    return 100 * sum(base.upper() in {"G", "C"} for base in sequence) / len(sequence)


def main():
    parser = argparse.ArgumentParser(
        description="Print the GC content of each record in a FASTA file."
    )
    parser.add_argument("fasta_file", help="path to the FASTA file")
    parser.add_argument(
        "--min-gc",
        type=float,
        help="only print records with GC content above or equal to this percentage",
    )
    args = parser.parse_args()

    for header, sequence in read_fasta_records(args.fasta_file):
        if not sequence:
            print(f"Warning: skipping empty FASTA sequence for >{header}", file=sys.stderr)
            continue
        gc = gc_percentage(sequence)
        if args.min_gc is not None and gc < args.min_gc:
            continue
        print(f">{header}: {gc:.2f}%")


if __name__ == "__main__":
    main()
