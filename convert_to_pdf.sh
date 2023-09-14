#!/bin/bash

svg_12_folder="generated_templates12/"
svg_18_folder="generated_templates18/"

src_dir=$svg_12_folder
dest_dir="converted_12/"
if [ ! -d "$dest_dir" ]; then
  mkdir -p "$dest_dir"
fi

# Loop through all SVG files in the source directory
for svg_file in "$src_dir"/*.svg; do
  if [ -f "$svg_file" ]; then
    # Extract the base filename without the extension
    base_name=$(basename -- "$svg_file" .svg)
    
    # Construct the PDF file path in the destination directory
    pdf_file="$dest_dir/$base_name.pdf"
    
    # Use Inkscape to convert SVG to PDF
    inkscape -o "$pdf_file" -d 300 "$svg_file"
    
    echo "Converted '$svg_file' to '$pdf_file'"
  fi
done