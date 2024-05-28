#! /bin/bash
set -e # exit on error

# check if filenames provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <filename1> <filename2> ..."
    exit 1
fi


# store number of parts in part_list
# part_list=()

# num_of_files=${#@}


# Initialize completed jobs
#completed_jobs=0

max_parallel=5
running_pids=()

# Function to check if a process is running
is_running() {
    local pid=$1
    ps -p $pid > /dev/null 2>&1
}


# Get the directory path of the script
script_dir=$(dirname "$0")
run_dir="$PWD"

# Set the path to the annotated genome database
db_path="$script_dir/annotated_genome_db"

for file in "$@"; do
    # get just the filename without path
    basename="${file##*/}"


    # get part number from filename
    part=$(echo $file | sed 's/.*.-//' | sed 's/.fasta//')
    name=$(echo $basename | sed 's/\.part.*/_/')
    output="$run_dir/$name$part.out"

    # process each file
    echo "Output: $output"
    echo "Processing $basename"

    

    nice -n 5 nohup tblastn -db $db_path -query $file -out $output -outfmt "7 qseqid sseqid pident ppos evalue bitscore salltitles" -evalue 1e-100 -num_threads 4 -max_target_seqs 10000 &
    pid=$!

    running_pids+=("$pid")

    #((completed_jobs+=1))

    #if [ "$completed_jobs" -eq "$max_parallel" ]; then
    #    wait -n
    #    ((completed_jobs-=1))
    #fi

    while [ "${#running_pids[@]}" -ge "$max_parallel" ]; do
        for job in "${!running_pids[@]}"; do
            if ! is_running "${running_pids[job]}"; then
                unset "running_pids[job]"
                break
            fi
        done
        sleep 1
    done

done

wait
echo "All files completed blast search"
