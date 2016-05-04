#!/bin/bash

#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --time=02:00:00 

#SBATCH --partition=training
#SBATCH --account=parallelcomputing
#SBATCH --exclusive

#SBATCH --job-name=ind
#SBATCH --output="individual.out.txt"


# Start time
START=$(date +%s.%N)


# Specify individual project, change based on selected project
project="chengchao0311_timeSqare_Calendar"

# Execute .jar on given project and save to output file
java -jar checkstyle-6.15-all.jar -c sun_checks.xml -o $project.out.txt localtmp/java_projects/$project

# Parse .jar output and overwrite the same output file
python style.py $project.out.txt


# End time
END=$(date +%s.%N)
# Total time
DIFF=$(echo "$END - $START" | bc)
echo "RUNTIME..." $DIFF