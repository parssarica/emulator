mov rax, 5
push rax
mov rbx, 7
push rbx
mul rax, rbx
pop rdx
pop rcx
mov rbx, 3
push rax
add rbx, rdx
mov rdx, rax
div rdx, rcx
mov rbx, rax
pop rax
sub rax, rbx
mov rbx, rax
mov rcx, rax
mov rdx, rax
mov rsi, rax
mov rdi, rax
