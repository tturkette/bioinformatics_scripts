import os
import tempfile
import pytest
from cluster_pathway_analysis import cluster_reader_dict_writer, pathways_reader_dict_writer, cluster_pathway_comparisons

# Test data files
clusters_file = "test_clusters.txt"
pathways_file = "test_pathways.txt"

# Example test data
clusters_data = """
Cluster1\tGeneA,GeneB,GeneC
Cluster2\tGeneD,GeneE
"""

pathways_data = """
Pathway1\tID1\tGeneA.1\tID123
Pathway2\tID2\tGeneB\tID456
"""

def create_temp_file(file_name, content):
    """Helper function to create temporary test files."""
    with open(file_name, 'w') as f:
        f.write(content)

@pytest.fixture
def setup_files():
    """Fixture to setup temporary test files."""
    create_temp_file(clusters_file, clusters_data)
    create_temp_file(pathways_file, pathways_data)

def test_cluster_reader_dict_writer(setup_files):
    """Test cluster_reader_dict_writer function."""
    expected_result = {
        'Cluster1': ['GeneA', 'GeneB', 'GeneC'],
        'Cluster2': ['GeneD', 'GeneE']
    }
    result = cluster_reader_dict_writer(clusters_file)
    assert result == expected_result

def test_pathways_reader_dict_writer(setup_files):
    """Test pathways_reader_dict_writer function."""
    expected_result = {
        'ID1': ['GeneA'],
        'ID2': ['GeneB']
    }
    result = pathways_reader_dict_writer(pathways_file)
    assert result == expected_result

def test_cluster_pathway_comparisons(setup_files):
    """Test cluster_pathway_comparisons function."""
    cluster_dict = {
        'Cluster1': ['GeneA', 'GeneB', 'GeneC'],
        'Cluster2': ['GeneD', 'GeneE']
    }
    pathways_dict = {
        'ID1': ['GeneA'],
        'ID2': ['GeneB']
    }
    expected_output = (
        "Pathway_cluster\tPC\tnPC\tPnC\tnPnC\n"
        "ID1_Cluster1\t1\t2\t0\t27677\n"
        "ID1_Cluster2\t0\t3\t0\t27677\n"
        "ID2_Cluster1\t1\t2\t0\t27677\n"
        "ID2_Cluster2\t1\t2\t0\t27677\n"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_output_file = os.path.join(temp_dir, 'test_output.txt')
        cluster_pathway_comparisons(cluster_dict, pathways_dict, temp_output_file)
        with open(temp_output_file, 'r') as f:
            result = f.read()
        assert result == expected_output

if __name__ == "__main__":
    pytest.main()