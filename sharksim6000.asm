.store "~~~~~~~~~~~~~~~~~~~~^~\x0d\x00"
mov rsi, 0x16
mov rbx, 1
mov rcx, [23]
sub rcx, rsi
mov rdx, rsi
mov rax, 4
int 80
mov rcx, 100000
push rax
mov rax, 0
cmp rcx, rax
dec rcx
jne 11
dec rsi
cmp rsi, rax
pop rax
jne 2
halt
