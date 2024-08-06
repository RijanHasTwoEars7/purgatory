#!/bin/bash

# check if the dependencies are present and available on path
command -v plink2 >/dev/null || { echo "This shell does not have access to plink2. Cowardly refusing to do what you asked for."; exit; }


input_file=$1
# get file base_names for later use
if [ -z "$2" ]; then
  output_name="${input_file%%.*}"
else
	output_name=$2
fi


plink2 --vcf $input_file --make-bed --out $output_name
