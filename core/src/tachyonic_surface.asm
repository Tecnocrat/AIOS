option casemap:none
PUBLIC aios_render_heightmap_ortho

.data

.code
; Windows x64 calling convention
aios_render_heightmap_ortho PROC
    ; RCX points, RDX count, R8 buffer, R9 width
    ; [rsp+40] height, [rsp+48] zScale, [rsp+56] baseColor
    push rbx
    push rsi
    push rdi
    sub rsp,32

    mov rsi, rcx
    mov rbx, rdx
    mov rdi, r8
    mov r12d, r9d
    mov r13d, DWORD PTR [rsp+32+40]
    mov r14d, DWORD PTR [rsp+32+56]

    test rbx, rbx
    jz done

next_point:
    movups xmm0, XMMWORD PTR [rsi] ; x y z ?
    mov eax, r12d
    dec eax
    cvtsi2ss xmm1, eax
    movss xmm2, xmm0
    mulss xmm2, xmm1
    cvtss2si edx, xmm2 ; X

    mov eax, r13d
    dec eax
    cvtsi2ss xmm3, eax
    shufps xmm0, xmm0, 0x55 ; y
    mulss xmm3, xmm0
    cvtss2si ecx, xmm3 ; Y

    cmp edx, r12d
    ja skip
    cmp ecx, r13d
    ja skip

    mov eax, ecx
    imul eax, r12d
    add eax, edx
    shl eax, 2
    mov edx, r14d
    mov DWORD PTR [rdi+rax], edx

skip:
    add rsi, 12
    dec rbx
    jnz next_point

done:
    add rsp,32
    pop rdi
    pop rsi
    pop rbx
    ret
aios_render_heightmap_ortho ENDP
END
