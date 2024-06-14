import subprocess

# Template SLURM script
slurm_script_template = '''#!/bin/bash

#SBATCH --time={time}       # how long the job will run (hh:mm:ss, or -t)
#SBATCH --ntasks={ntasks}   # how many nodes that you require (or -n)
#SBATCH --cpus-per-task={cpus_per_task}   # number of CPUs (or cores) per task (or -c)
#SBATCH --mem={memory}      # memory required/node (in bytes)
#SBATCH --job-name={job_name}    # job name for easier identification (or -J)

########## Command Lines to Run ##########

### call your executable

time ~/bin/myblast/bin/blastp -query {query_file} -task blastp \
-evalue 1e-10 -seg yes -word_size 3 -db {db_location} -out {output_file} -outfmt 6

### write job information to output file

scontrol show job $SLURM_JOB_ID
'''

def generate_slurm_script(time, ntasks, cpus_per_task, memory, your_name, query_file, db_location, output_file):
    """
    Generate a SLURM script with specified parameters.
    
    Parameters:
    - time (str): Time duration for the job (hh:mm:ss).
    - ntasks (int): Number of nodes required.
    - cpus_per_task (int): Number of CPUs (or cores) per task.
    - memory (str): Memory required per node (in bytes).
    - your_name (str): Name to incorporate into job name.
    - query_file (str): Location of the query fasta file.
    - db_location (str): Location of the protein database.
    - output_file (str): Output file name for BLAST results.
    
    Returns:
    - str: Generated SLURM script as a string.
    """
    job_name = f"run_blast_{your_name}"
    
    slurm_script = slurm_script_template.format(
        time=time,
        ntasks=ntasks,
        cpus_per_task=cpus_per_task,
        memory=memory,
        job_name=job_name,
        query_file=query_file,
        db_location=db_location,
        output_file=output_file
    )
    return slurm_script

def submit_slurm_job(slurm_script):
    """
    Submit a SLURM job using the provided SLURM script.
    
    Parameters:
    - slurm_script (str): SLURM script content as a string.
    
    Raises:
    - subprocess.CalledProcessError: If the sbatch command returns a non-zero exit status.
    """
    try:
        # Write the SLURM script to a temporary file
        with open('submit_script.sh', 'w') as f:
            f.write(slurm_script)
        
        # Submit the SLURM script using sbatch command
        process = subprocess.run(['sbatch', 'submit_script.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        # Print the output from sbatch
        print("Submitted SLURM job. Output:")
        print(process.stdout.decode())
        if process.stderr:
            print("Errors encountered:")
            print(process.stderr.decode())

    except subprocess.CalledProcessError as e:
        # Log the error if sbatch command fails
        print(f"Error submitting SLURM job: {e}")
        raise e

    finally:
        # Clean up: remove the temporary script file
        subprocess.run(['rm', 'submit_script.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Example usage:
if __name__ == "__main__":
    time = "00:30:00"
    ntasks = 1
    cpus_per_task = 1
    memory = "1G"
    your_name = "SMITH"  # Replace with your actual name
    query_file = "<.fa-file-location>"
    db_location = "<prot-db-location>"
    output_file = "<output-file-name>"

    slurm_script = generate_slurm_script(time, ntasks, cpus_per_task, memory, your_name, query_file, db_location, output_file)
    submit_slurm_job(slurm_script)
