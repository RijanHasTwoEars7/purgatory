#!/bin/bash

# we will just take the first file from the CLI as the input

input_file="$1"

# if you do not know the extension of the file use this to get the basename
base_name="$(basename -- $input_file)"
base_name="${base_name%.*}"

sort_file_list="${base_name}.sorted_lines"

bcftools query -l $input_file | sort > $sort_file_list

bcftools view -S $sort_file_list $input_file -o "${base_name}.vcf"

rm $sort_file_list
