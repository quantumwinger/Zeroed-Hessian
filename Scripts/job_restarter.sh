#!/bin/bash

mkdir iter
cd iter

input_files=($(ls ../*.inp))

for input_file in "${input_files[@]}"; do
  input_name="${input_file%.*}"
 echo ${input_name}.out
 vvar=$(grep 'OPTIMIZATION CONVERGED' ../${input_name}.out | wc -l)
        if [ $vvar -eq  1 ]
        then
                echo "good"
        else
                echo "bad"
		sed '/Displacement from previous Coordinates is:/,/Molecular Point Group/!d' ../${input_name}.out | csplit -z - '/Molecular Point Group/1' '{*}'
		cp `ls -rt xx* | head -1` $PWD/${input_name}.txt
		rm xx*
		sed -i '1,5d' ${input_name}.txt
        	head -n -2 ${input_name}.txt > ${input_name}.xyz
		rm ${input_name}.txt
		awk '{$1=""; print $0}' ${input_name}.xyz > testfile.tmp && mv testfile.tmp ${input_name}.xyz
		cp ../${input_name}.job .
        fi
done
cd ../
