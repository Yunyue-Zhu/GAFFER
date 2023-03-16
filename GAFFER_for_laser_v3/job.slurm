#!/bin/bash

#SBATCH --job-name=GaMULTIz       # Name
#SBATCH --partition=cpu           # cpu 
#SBATCH -n 80                     # total cpu 
#SBATCH --ntasks-per-node=40      # cpu/node
#SBATCH --get-user-env
#SBATCH --output=%j.out
#SBATCH --error=%j.err 

python3 main.py > result.txt

echo "0.00" > inp_0.dat
cat result.txt | tail -n 27 | head -n 24 >> inp_0.dat
echo "0.00" >> inp_0.dat
tail -3 result.txt >> inp_0.dat
./multi_fin 0
