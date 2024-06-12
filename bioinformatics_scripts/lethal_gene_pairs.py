import os
import logging

def lethal_gene_pairs(file, lethality_threshold, output_dir='.'):
    """
    This function takes a tab-delimited file in the format gene1\tgene2\tlethality and
    a lethality threshold as input and writes two text files: one for gene pairs that exceed
    the threshold and another for gene pairs that are below the threshold.

    Parameters:
        file (str): Path to the input tab-delimited file.
        lethality_threshold (float): Threshold for lethality to categorize gene pairs.
        output_dir (str): Directory where output files will be saved. Default is the current directory.

    Raises:
        ValueError: If the input file is not formatted correctly or contains invalid data.
        IOError: If the input file cannot be read or the output files cannot be written.
    """
    logging.basicConfig(level=logging.INFO)
    
    # Check if input file exists
    if not os.path.isfile(file):
        logging.error("Input file not found: %s", file)
        raise IOError(f"File not found: {file}")
    
    # Check if output directory exists and is writable
    if not os.path.isdir(output_dir):
        logging.error("Output directory does not exist: %s", output_dir)
        raise IOError(f"Output directory does not exist: {output_dir}")
    if not os.access(output_dir, os.W_OK):
        logging.error("Output directory is not writable: %s", output_dir)
        raise IOError(f"Output directory is not writable: {output_dir}")

    above_threshold = []
    below_threshold = []

    try:
        with open(file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split('\t')
                if len(parts) != 3:
                    logging.error("Invalid line format: %s", line)
                    raise ValueError(f"Invalid line format: {line}")
                gene1, gene2, lethality_str = parts
                try:
                    lethality = float(lethality_str)
                except ValueError:
                    logging.error("Invalid lethality value: %s", lethality_str)
                    raise ValueError(f"Invalid lethality value: {lethality_str}")
                
                if lethality >= lethality_threshold:
                    above_threshold.append((gene1, gene2))
                else:
                    below_threshold.append((gene1, gene2))
        
        above_threshold_file = os.path.join(output_dir, 'above_threshold.txt')
        below_threshold_file = os.path.join(output_dir, 'below_threshold.txt')

        with open(above_threshold_file, 'w') as f:
            for pair in above_threshold:
                f.write(f"{pair[0]}\t{pair[1]}\n")
        
        with open(below_threshold_file, 'w') as f:
            for pair in below_threshold:
                f.write(f"{pair[0]}\t{pair[1]}\n")

        logging.info("Processing complete. Results saved in %s and %s", 
                     above_threshold_file, below_threshold_file)

    except IOError as e:
        logging.error("An IOError occurred: %s", str(e))
        raise
    except Exception as e:
        logging.error("An unexpected error occurred: %s", str(e))
        raise