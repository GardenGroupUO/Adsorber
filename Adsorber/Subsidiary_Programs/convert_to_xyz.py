#!/usr/bin/env python3

import sys
from ase.io import read, write

input_name  = sys.argv[1]
output_name = sys.argv[2]

system = read(input_name)
write(output_name,system)
print('Converted '+str(input_name)+' to '+str(output_name))