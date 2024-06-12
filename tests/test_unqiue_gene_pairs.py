import os
import pickle
import tempfile
import pytest
from unique_gene_pairs import unique_gene_pairs

def test_unique_gene_pairs():
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tempdir:
        # Create a temporary input file
        input_file = os.path.join(tempdir, 'input.txt')
        with open(input_file, 'w') as f:
            f.write("gene1\tgene2\tvalue1\tvalue2\n")
            f.write("gene1\tgene3\tvalue3\tvalue4\n")
            f.write("gene1\tgene2\tvalue5\tvalue6\n")
            f.write("gene4\tgene5\tvalue7\tvalue8\n")
        
        # Run the function
        output_file, pickle_file = unique_gene_pairs(input_file, tempdir)
        
        # Verify the output file content
        with open(output_file, 'r') as f:
            content = f.readlines()
        
        assert content[0].strip() == "Number of unique gene pairs: 3"
        assert "gene1\tgene2\tvalue1,value2\n" in content
        assert "gene1\tgene3\tvalue3,value4\n" in content
        assert "gene4\tgene5\tvalue7,value8\n" in content
        
        # Verify the pickle file content
        with open(pickle_file, 'rb') as f:
            unique_gene_pairs_data = pickle.load(f)
        
        assert unique_gene_pairs_data == {
            'gene1': [('gene2', ['value1', 'value2']), ('gene3', ['value3', 'value4'])],
            'gene4': [('gene5', ['value7', 'value8'])]