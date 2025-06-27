mov rax, 2
mov rbx, 3
add rax, rbx
fnc mul_by_three
mov rcx, rax
mov rdx, 0
mov rbx, 2
dec rbx
add rax, rcx
cmp rbx, rdx
jne 7
ret rax
gip
mov rdx, 6
add rax, rdx
push rax
mov rax, 5
call mul_by_three
mov rbx, rax
halt
