fnc a
mov rbx, 2
mov rcx, 879679
mul rbx, rcx
ret rax
fnc b
mov rbx, 788
mov rcx, 8967
mul rbx, rcx
mov rbx, 100
call a
mul rax, rax
ret rax
nop
call b
halt
