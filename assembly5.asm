fnc sleep
mov rax, 5
dec rax
mov rbx, 0
cmp rax, rbx
jne 2
ret rax
fnc laser
mov rbp, 1
mov rsp, 4
mov rax, -1
mov rbx, 0
push rax
push rbx
nop
pop rbx
pop rax
inc rax
tgl rax
mov rcx, 0
cmp rbx, rcx
je 22
mov rcx, 8
cmp rax, rcx
je 32
inc rax
inc rbx
mov rdx, 13
push rax
push rbx
push rdx
call sleep
ret rax
gip
mov rbx, 5
add rax, rbx
push rax
call laser
halt
