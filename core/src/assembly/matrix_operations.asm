
; High-performance 4x4 matrix multiplication
; Input: RDI = matrix A, RSI = matrix B, RDX = result matrix
; Uses SSE/AVX instructions for SIMD optimization

section .text
global matrix_multiply_4x4

matrix_multiply_4x4:
    ; Save registers
    push rbp
    mov rbp, rsp
    
    ; Load first row of matrix A into XMM registers
    movups xmm0, [rdi]      ; A[0][0-3]
    movups xmm1, [rdi+16]   ; A[1][0-3]
    movups xmm2, [rdi+32]   ; A[2][0-3]
    movups xmm3, [rdi+48]   ; A[3][0-3]
    
    ; Multiply and accumulate for each column of B
    xor rcx, rcx            ; Column counter
    
.column_loop:
    ; Load column from matrix B
    movss xmm4, [rsi + rcx*4]       ; B[0][col]
    movss xmm5, [rsi + rcx*4 + 16]  ; B[1][col]
    movss xmm6, [rsi + rcx*4 + 32]  ; B[2][col]
    movss xmm7, [rsi + rcx*4 + 48]  ; B[3][col]
    
    ; Broadcast and multiply
    shufps xmm4, xmm4, 0x00  ; Broadcast B[0][col]
    shufps xmm5, xmm5, 0x00  ; Broadcast B[1][col]
    shufps xmm6, xmm6, 0x00  ; Broadcast B[2][col]
    shufps xmm7, xmm7, 0x00  ; Broadcast B[3][col]
    
    mulps xmm4, xmm0        ; A[0] * B[0][col]
    mulps xmm5, xmm1        ; A[1] * B[1][col]
    mulps xmm6, xmm2        ; A[2] * B[2][col]
    mulps xmm7, xmm3        ; A[3] * B[3][col]
    
    ; Sum the results
    addps xmm4, xmm5
    addps xmm6, xmm7
    addps xmm4, xmm6
    
    ; Store result column
    movups [rdx + rcx*16], xmm4
    
    inc rcx
    cmp rcx, 4
    jl .column_loop
    
    ; Restore registers
    pop rbp
    ret
