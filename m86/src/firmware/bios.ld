OUTPUT_ARCH(i8086)

main_address = 4096M - 4K;              /* Use the last 4K block                   */

MEMORY {
        ROM (rx) : org = 4096M - 64K, len = 64K
}

SECTIONS {
        ENTRY(init)
        .begin : {      
                *(begin)
        } >ROM          
        .main main_address : {
                *(main)
        }
        .reset 4096M - 0x10 : {         
                *(reset)
        }
}
