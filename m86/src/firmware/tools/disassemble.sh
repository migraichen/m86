#!/bin/bash

objdump -D -b binary -mi386 -Maddr16,data16 --start-address $1 bios.rom | head -n 20
