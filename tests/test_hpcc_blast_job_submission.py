import pytest
from blast_slurm_submit import generate_slurm_script, submit_slurm_job

def test_generate_slurm_script():
    time = "00:30:00"
    ntasks = 1
    cpus_per_task = 1
    memory = "1G"
    variable_name = "SMITH"  # Example variable name, replace with your actual variable
    query_file = "<.fa-file-location>"
    db_location = "<prot-db-location>"
    output_file = "<output-file-name>"
    
    slurm_script = generate_slurm_script(time, ntasks, cpus_per_task, memory, variable_name, query_file, db_location, output_file)
    
    assert "#SBATCH --time=00:30:00" in slurm_script
    assert "#SBATCH --ntasks=1" in slurm_script
    assert "#SBATCH --cpus-per-task=1" in slurm_script
    assert "#SBATCH --mem=1G" in slurm_script
    assert f"#SBATCH --job-name=run_blast_{variable_name}" in slurm_script
    assert f"~/bin/myblast/bin/blastp -query {query_file}" in slurm_script
    assert f"-db {db_location}" in slurm_script
    assert f"-out {output_file}" in slurm_script
    assert "-outfmt 6" in slurm_script


if __name__ == "__main__":
    pytest.main()