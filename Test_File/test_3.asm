 .data                   
     value1:     .word 12     # First value in memory (12 -> 0b1100)
   	     value2:     .word 10     # Second value in memory (10 -> 0b1010)
        .text                   	
    lw $t0, value1       # $t0 = value1 (12 -> 0b1100)
    lw $t1, value2       # $t1 = value2 (10 -> 0b1010)
    and $t2, $t0, $t1    # $t2 = $t0 & $t1 (0b1100 & 0b1010 = 0b1000 -> 8)
