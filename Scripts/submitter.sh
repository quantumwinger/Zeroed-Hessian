#!/bin/bash

module load python

python frozen.py reac.xyz opt
python frozen.py ts.xyz  ts
python frozen.py prod.xyz opt

input_files=($(ls *.inp))
template_file="template.job"

for input_file in "${input_files[@]}"; do
  input_name="${input_file%.*}"

  sed "s/template/$input_name/g" "$template_file" > "$input_name.job"

  echo "Created $input_name.job"
  #sbatch $input_name.job
done

