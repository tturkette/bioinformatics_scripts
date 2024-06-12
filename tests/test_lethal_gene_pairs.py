import os
import tempfile
import pytest
from lethal_gene_pairs import lethal_gene_pairs

def test_lethal_gene_pairs():
    lethality_threshold = 0.5

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tempdir:
        # Create a temporary input file
        input_file = os.path.join(tempdir, 'input.txt')
        with open(input_file, 'w') as f:
            f.write("gene1\tgene2\t0.4\n")
            f.write("gene3\tgene4\t0.6\n")
            f.write("gene5\tgene6\t0.5\n")
            f.write("gene7\tgene8\t0.3\n")

        # Run the function
        try:
            lethal_gene_pairs(input_file, lethality_threshold, tempdir)

            # Verify the output files content
            above_threshold_file = os.path.join(tempdir, 'above_threshold.txt')
            below_threshold_file = os.path.join(tempdir, 'below_threshold.txt')

            # Check if above_threshold.txt exists and contains the correct pairs
            with open(above_threshold_file, 'r') as f:
                above_content = f.readlines()
                assert "gene3\tgene4\n" in above_content
                assert "gene5\tgene6\n" in above_content

            # Check if below_threshold.txt exists and contains the correct pairs
            with open(below_threshold_file, 'r') as f:
                below_content = f.readlines()
                assert "gene1\tgene2\n" in below_content
                assert "gene7\tgene8\n" in below_content

        except Exception as e:
            pytest.fail(f"Test failed with exception: {e}")
