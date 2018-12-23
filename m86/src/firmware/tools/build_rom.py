#!/usr/bin/env python3
"""
Generates a 1MB 16-bit VHDL-Array from a Binary input.
"""
#import sys
#import getopt
import argparse
import binascii
import struct
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', action='store', dest='ifile', help='input file', default='bios.rom')
    parser.add_argument('-o', action='store', dest='ofile', help='output file', default='obj_code_pkg.vhdl')
    args = parser.parse_args()
    
    # Write the header of the VHDL file
    oobj = open(args.ofile, "w")
    oobj.write("----------------------------------------------------------------------------------\n")
    oobj.write("-- obj_code_pkg.vhdl -- Application object code in vhdl constant string format. --\n")
    oobj.write("----------------------------------------------------------------------------------\n")
    oobj.write("\n")
    oobj.write("library ieee;\n")
    oobj.write("use ieee.std_logic_1164.all;\n")
    oobj.write("use ieee.numeric_std.all;\n")
    oobj.write("\n")
    oobj.write("package obj_code_pkg is\n")
    oobj.write("\n")
    oobj.write("-- Object code initialization constant.\n")
    oobj.write("constant object_code : t_obj_code(0 to 1048575) := (\n")

    segment = 0
    offset = 0
    # Write Segment 0 to E
    for i in range(0, 15):
        oobj.write("  -- Segment {:x} \n".format(segment))
        
        # Segment is 64kB with 16 bytes per line
        for i in range(0, int((64*1024)/16)):
            line = "  "        
            for j in range(0, 8):
                line += "X\"0000\", "

            line += "-- {:08x}\n".format(offset)
            offset += 16

            oobj.write(line)
        segment += 1 

    # Write Segment F
    oobj.write("  -- Segment {:x} \n".format(segment))
    iobj = open(args.ifile, "rb")

    # Segment is 64kB with 16 bytes per line
    for i in range(0, int((64*1024)/16)):
        line = "  "
        # 16 Bytes per line but we read two Bytes each loop so eight turn in this loop 
        for j in range(0, 8):
            l = iobj.read(1)
            h = iobj.read(1)
            line += "X\"{0:02x}{1:02x}\", ".format(ord(h),ord(l))


        line += "-- {:08x}\n".format(offset)
        offset += 16

        oobj.write(line)    
    
    iobj.close();

    # Del the last comma to avoid an VHDL Error
    position = oobj.tell() 
    oobj.seek(oobj.tell()-14)
    oobj.write(" ")
    oobj.seek(position)

    # Write the end of the VHDL file    
    oobj.write(");\n")
    oobj.write("\n")
    oobj.write("end package obj_code_pkg;\n")

    oobj.close();
