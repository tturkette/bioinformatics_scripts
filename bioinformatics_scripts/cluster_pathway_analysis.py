import sys
import os
import logging
from typing import Dict, List

def cluster_reader_dict_writer(file_path: str) -> Dict[str, List[str]]:
    """
    Reads a file containing gene clusters and outputs a dictionary.

    Args:
        file_path (str): Path to the input file containing clusters data.

    Returns:
        Dict[str, List[str]]: A dictionary with cluster IDs as keys and lists of genes as values.

    Raises:
        IOError: If the file cannot be read.
        ValueError: If the file format is incorrect.
    """
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except IOError:
        logging.error(f"File not found: {file_path}")
        raise IOError(f"File not found: {file_path}")

    cluster_dict = {}
    for line in lines[1:]:  # skip header
        line = line.strip()
        if line:
            parts = line.split("\t")
            if len(parts) < 2:
                raise ValueError(f"Invalid line format: {line}")
            cluster_id = parts[0]
            gene_list = parts[1].split(',')
            cluster_dict[cluster_id] = gene_list

    return cluster_dict

def pathways_reader_dict_writer(file_path: str) -> Dict[str, List[str]]:
    """
    Reads a file containing gene-pathway associations and outputs a dictionary.

    Args:
        file_path (str): Path to the input file containing pathways data.

    Returns:
        Dict[str, List[str]]: A dictionary with pathway IDs as keys and lists of genes as values.

    Raises:
        IOError: If the file cannot be read.
        ValueError: If the file format is incorrect.
    """
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except IOError:
        logging.error(f"File not found: {file_path}")
        raise IOError(f"File not found: {file_path}")

    pathway_dict = {}
    for line in lines[1:]:  # skip header
        line = line.strip()
        if line:
            parts = line.split("\t")
            if len(parts) != 4:
                raise ValueError(f"Invalid line format: {line}")
            pathway_id = parts[1]
            gene_name = parts[2].split('.')[0].upper()
            gene_id = parts[3].split('.')[0].upper()
            gene = gene_id if gene_id.startswith("AT") else gene_name

            if gene.startswith("AT") and gene[2] == 'G':
                if pathway_id not in pathway_dict:
                    pathway_dict[pathway_id] = []
                if gene not in pathway_dict[pathway_id]:
                    pathway_dict[pathway_id].append(gene)

    return pathway_dict

def cluster_pathway_comparisons(cluster_dict: Dict[str, List[str]], pathway_dict: Dict[str, List[str]]) -> None:
    """
    Compares genes in pathways and clusters and writes the results to a file.

    Args:
        cluster_dict (Dict[str, List[str]]): Dictionary containing the cluster genes as values keyed to the cluster number.
        pathway_dict (Dict[str, List[str]]): Dictionary containing the pathway genes as values keyed to the pathway ID.
    """
    output_buffer = 'Pathway_cluster\tPC\tnPC\tPnC\tnPnC\n'
    total_genes = 27680  # Total number of genes in Arabidopsis thaliana

    for pathway_id, pathway_genes in pathway_dict.items():
        for cluster_id, cluster_genes in cluster_dict.items():
            shared_genes = set(cluster_genes).intersection(pathway_genes)
            pc = len(shared_genes)
            npc = len(cluster_genes) - pc
            pnc = len(pathway_genes) - pc
            npnc = total_genes - pc - npc - pnc

            output_buffer += f'{pathway_id}_{cluster_id}\t{pc}\t{npc}\t{pnc}\t{npnc}\n'

    with open('pathway_counts.txt', 'w') as output_file:
        output_file.write(output_buffer)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        logging.error("Usage: cluster_pathway_analysis.py <clusters_file> <pathways_file>")
        sys.exit(1)

    clusters_file = sys.argv[1]
    pathways_file = sys.argv[2]

    c_dict = cluster_reader_dict_writer(clusters_file)
    p_dict = pathways_reader_dict_writer(pathways_file)
    cluster_pathway_comparisons(c_dict, p_dict)