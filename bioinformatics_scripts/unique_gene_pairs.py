
import pickle
import os
import logging

def contains_gene(dictionary, key, target_gene):
     """
    Check if a target gene is contained within one of the tuples in the list keyed to a specific gene.

    Args:
        dictionary (dict): A dictionary where keys are genes and values are lists of tuples. 
                           Each tuple contains a gene and associated values.
        key (str): The gene whose list of tuples is to be checked.
        target_gene (str): The gene to search for within the list of tuples.

    Returns:
        bool: True if the target gene is found within the tuples of the specified key, False otherwise.
    """
     return any(target_gene == gene for gene, _ in dictionary.get(key, []))

def unique_gene_pairs(filename, output_dir):
    """
    Process a file containing gene pairs and their associated values, and produce
    an output file and a pickle file with unique gene pairs.

    Args:
        filename (str): Path to the input file containing gene pairs and values.
        output_dir (str): Path to the directory where the output files will be saved.

    Raises:
        IOError: If the input file is not found or the output directory is not writable.
        ValueError: If a line in the input file does not have the expected format.

    Returns:
        tuple: Paths to the output text file and the output pickle file.
    """
    logging.basicConfig(level=logging.INFO)

    # Check if input file exists
    if not os.path.isfile(filename):
        logging.error("Input file not found: %s", filename)
        raise IOError(f"File not found: {filename}")
    
    # Check if output directory exists and is writable
    if not os.path.isdir(output_dir):
        logging.error("Output directory does not exist: %s", output_dir)
        raise IOError(f"Output directory does not exist: {output_dir}")
    if not os.access(output_dir, os.W_OK):
        logging.error("Output directory is not writable: %s", output_dir)
        raise IOError(f"Output directory is not writable: {output_dir}")
    
    unique_gene_pairs = {}
    unique_gene_pairs_counter = 0

    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split('\t')
                if len(parts) < 2:
                    logging.error("Invalid line format: %s", line)
                    raise ValueError(f"Invalid line format: {line}")
                gene1 = parts[0]
                gene2 = parts[1]
                values = parts[2:]  # Values are all parts after the first two
                
                if gene1 not in unique_gene_pairs:
                    unique_gene_pairs[gene1] = [(gene2, values)]
                    unique_gene_pairs_counter += 1
                elif not contains_gene(unique_gene_pairs, gene1, gene2):
                    unique_gene_pairs[gene1].append((gene2, values))
                    unique_gene_pairs_counter += 1
    except IOError:
        logging.error("Error reading file: %s", filename)
        raise IOError(f"Error reading file: {filename}")

    output_file = os.path.join(output_dir, 'unique_gene_pairs.txt')
    with open(output_file, 'w') as f:
        f.write(f"Number of unique gene pairs: {unique_gene_pairs_counter}\n")
        for gene1, pairs in unique_gene_pairs.items():
            for gene2, values in pairs:
                f.write(f"{gene1}\t{gene2}\t{','.join(values)}\n")
    
    pickle_file = os.path.join(output_dir, 'unique_gene_pairs.pkl')
    with open(pickle_file, 'wb') as f:
        pickle.dump(unique_gene_pairs, f)
    
    return output_file, pickle_file