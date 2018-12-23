/* BIOS Demo
                                                                       
   Jumps from the resetvector to the init-routine 
   clears the AX register and puts 0x01 to the debug port  
   and end up in an endless loop    

   There are only 6 instructions to be implemented for the beginning 
   to test the hardware and the toolchain
                                                                        */

.intel_syntax noprefix              
.code16                            

DEBUG_PORT    = 0x80

.section begin, "a"                 
        .ascii "BIOS v0.01"    
        .align 16, 0xff


.section main, "ax"
.globl init                        
init:                               
        xor ax, ax
        mov al, 0x01 
        out DEBUG_PORT, al

loop:
        jmp loop

.section reset, "ax"
        /* Issue a manual jmp to work around a binutils bug.                    */
        /* See coreboot's src/cpu/x86/16bit/reset16.inc                         */
        cli
        .byte  0xe9
        .int   init - ( . + 2 )
        .ascii "22/09/18"
        .align 16, 0xff

