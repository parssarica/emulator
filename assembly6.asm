fnc sleep
mov rax, 5
mov rbx, 0
dec rax
cmp rax, rbx
jne 3
ret rax
fnc rocket
mov rcx, 4
tgl 0
gip
add rax, rcx
push rax
call sleep
tgl 0
tgl 1
gip
add rax, rcx
push rax
call sleep
tgl 1
tgl 2
gip
add rax, rcx
push rax
call sleep
tgl 2
tgl 3
gip
add rax, rcx
push rax
call sleep
tgl 3
tgl 4
gip
add rax, rcx
push rax
call sleep
tgl 4
tgl 5
gip
add rax, rcx
push rax
call sleep
tgl 5
tgl 6
gip
add rax, rcx
push rax
call sleep
tgl 6
tgl 7
gip
add rax, rcx
push rax
call sleep
tgl 7
ret rax
gip
mov rbx, 5
add rax, rbx
push rax
call rocket
halt
