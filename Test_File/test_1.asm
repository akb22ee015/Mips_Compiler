.data
    num1:   .word 25
    num2:   .word 10
.text
    lw $t0, num1        # Load num1 into $t0
    lw $t1, num2        # Load num2 into $t1
    sub $t2, $t0, $t1   # $t2 = $t0 - $t1

