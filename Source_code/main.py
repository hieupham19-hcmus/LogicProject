import argparse
import os

from PLResolution import PLResolution
from Utilities import read_file

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run PL-resolution with input and output file paths or directory.')
    parser.add_argument('-i', '--input', help='Input file or directory path')
    parser.add_argument('-o', '--output', help='Output file or directory path')
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output

    if os.path.isdir(input_path):
        for file_name in os.listdir(input_path):
            if file_name.endswith('.txt'):
                input_file = os.path.join(input_path, file_name)
                if output_path and os.path.isfile(output_path):
                    output_file = output_path
                else:
                    output_file = os.path.join(output_path, f"{os.path.splitext(file_name)[0]}_output.txt")
                KB, alpha = read_file(input_file)
                PL = PLResolution()
                check = PL.pl_resolution(KB, alpha, output_file)
    else:
        KB, alpha = read_file(input_path)
        output_file = output_path if output_path else "output.txt"
        PL = PLResolution()
        check = PL.pl_resolution(KB, alpha, output_file)
