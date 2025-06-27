fnc tgl_x
tgl rax
mov rcx, 0
mov rbx, 11
dec rbx
cmp rbx, rcx
jne 4
tgl rax
imp 0
push rax
mov rbx, 64684
mov rcx, 46847
mul rbx, rcx
mov rcx, 4
div rax, rcx
pop rbx
sub rbx, rax
ret rax
mov rax, 32
call tgl_x
mov rbx, rax
mov rcx, rax
mov rdx, rax
mov rsi, rax
mov rdi, rax
halt
