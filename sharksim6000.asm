.store "~~~~~~~~~~~~~~~~~~~~^~\x0d\x00"
mov rsi, 0x16
mov rbx, 1
mov rcx, [23]
sub rcx, rsi
mov rdx, rsi
mov rax, 4
int 80
mov rcx, 100000
loop 9
dec rsi
push rax
mov rax, 0
cmp rsi, rax
pop rax
jne 2
mov rbx, 0
mov rax, 1
int 80
