; x64 MASM implementation (Windows ABI)
option casemap:none
PUBLIC aios_render_heightmap_ortho

.data
one REAL4 1.0

.code
; Windows x64 calling convention:
; RCX, RDX, R8, R9 = first four params
; Stack (8+): others
; void aios_render_heightmap_ortho(
;   const float* pointsXYZ,   RCX
;   uint32_t pointCount,      RDX
;   uint8_t* pixelBuffer,     R8
;   uint32_t width,           R9
;   uint32_t height,          [rsp+40]
;   float zScale,             [rsp+48]
;   uint32_t baseColor        [rsp+56]
; )
aios_render_heightmap_ortho PROC
    push rbx
    push rsi
    push rdi
    sub rsp, 32                ; shadow space + align

    mov rsi, rcx               ; points
    mov rbx, rdx               ; pointCount
    mov rdi, r8                ; pixelBuffer
    mov r12d, r9d              ; width
    mov r13d, DWORD PTR [rsp+32+40] ; height
    mov r14d, DWORD PTR [rsp+32+56] ; baseColor
    movss xmm7, DWORD PTR [rsp+32+48] ; zScale

    test rbx, rbx
    jz done

next_point:
    ; load x,y,z
    movups xmm0, XMMWORD PTR [rsi] ; x y z ?
    ; compute pixel x
    mov eax, r12d
    dec eax
    cvtsi2ss xmm1, eax
    movss xmm2, xmm0
    mulss xmm2, xmm1
    cvtss2si edx, xmm2          ; X
    ; compute pixel y
    mov eax, r13d
    dec eax
    cvtsi2ss xmm3, eax
    shufps xmm0, xmm0, 0x55     ; y
    mulss xmm3, xmm0
    cvtss2si ecx, xmm3          ; Y
    ; z brightness (ignored for now, future shading)

    ; bounds check
    cmp edx, r12d
    ja skip
    cmp ecx, r13d
    ja skip
    ; offset = (Y * width + X) * 4
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
    add rsp, 32
    pop rdi
    pop rsi
    pop rbx
    ret
aios_render_heightmap_ortho ENDP

END
