mov rbx, 1
mov rcx, 2
add rbx, rcx
mov rbx, 0
mov rdx, 16384
nop
nop
nop
nop
nop
mul rdx, rcx
mov rdx, rax
cmp rdx, rax
jne 0
je 16
halt
add rax, rdx
mov rbx, 49152
cmp rbx, rax
jmp 15
