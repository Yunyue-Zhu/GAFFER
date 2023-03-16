#!/bin/bash

#SBATCH --job-name=GaMULTIz       # Name
#SBATCH --partition=cpu           # cpu 
#SBATCH -n 80                     # total cpu 
#SBATCH --ntasks-per-node=40      # cpu/node
#SBATCH --get-user-env
#SBATCH --output=%j.out
#SBATCH --error=%j.err 

python3 main.py > result.txt
