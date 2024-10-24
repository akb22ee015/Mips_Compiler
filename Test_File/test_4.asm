.data
    num1: .word 12
    num2: .word 10
.text
    lw $t0, num1         
    lw $t1, num2 
    add $t5, $t0, $t1        
    sub $t6, $t0, $t1        
    and $t2, $t0, $t1    
    or  $t3, $t0, $t1  
    slt $t4, $t2, $t3   
