ASM       = gcc
LD        = ld
OBJCOPY   = objcopy

CFLAGS    = -m32
LDFLAGS   = -nostartfile

OBJECTS   = bios.o
TARGET    = bios
MEMLAYOUT = xMemLayout.map
VHDL_FILE = obj_code_pkg.vhdl

.PHONY: all clean

all: $(TARGET).rom package

clean:
	rm -f -v *.o $(TARGET).out $(TARGET).rom $(MEMLAYOUT) $(VHDL_FILE)

%.o: %.S Makefile
	$(ASM) -c -o $*.o $(CFLAGS) $<

$(TARGET).out: $(OBJECTS) $(TARGET).ld
	$(LD) $(LDFLAGS) -T$(TARGET).ld -o $@ $(OBJECTS) -Map $(MEMLAYOUT)

$(TARGET).rom: $(TARGET).out
	$(OBJCOPY) -O binary -j .begin -j .main -j .reset --gap-fill=0x0ff $< $@

package: bios.rom
	@echo Building object code VHDL package...
	@python3 tools/build_rom.py \
		-f $(TARGET).rom  \
		-o $(VHDL_FILE)

