#!/bin/bash

# check if the dependencies are present and available on path
command -v plink2 >/dev/null || { echo "Cowardly refusing to do what you asked because this shell does not have access to plink2"; exit; }

output_directory="plink_bulk_output"

# CLI flags
while test $# -gt 0; do
  case "$1" in
    -i|--input_directory)
      shift
      input_directory="$1"
      shift
      ;;
    -o|--output_directory)
      shift
      output_directory=$1
      shift
      ;;
    *)
      # Handle other flags or break out of the loop
      break
      ;;
  esac
done

if [[ ! -d "$output_directory" ]]; then
    mkdir -p "$output_directory"
fi

echo "Please note that this script uses .vcf extension to determine what files should be converted."

for vcf_file in "$input_directory"/*
do
	# if you do not know the extension of the file use this to get the basename
	base_name="$(basename -- $vcf_file)"
	base_name="$(echo "$base_name" | sed -E 's/^(.*)\.[^.]*$/\1/')"
	# replace . in the name because plink is particular about that
	base_name="${base_name//./_}"

	# call plink2
	plink2 --vcf $vcf_file --make-bed --out "${output_directory}/${base_name}"
done
