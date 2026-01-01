
; High-performance vector operations
; Optimized for real-time 3D calculations

section .text
global vector_cross_product
global vector_dot_product
global vector_normalize

vector_cross_product:
    ; Input: RDI = vector A, RSI = vector B, RDX = result
    ; Cross product: A x B = (AyBz - AzBy, AzBx - AxBz, AxBy - AyBx)
    
    movss xmm0, [rdi]       ; Ax
    movss xmm1, [rdi+4]     ; Ay
    movss xmm2, [rdi+8]     ; Az
    movss xmm3, [rsi]       ; Bx
    movss xmm4, [rsi+4]     ; By
    movss xmm5, [rsi+8]     ; Bz
    
    ; Calculate cross product components
    movss xmm6, xmm1        ; Ay
    mulss xmm6, xmm5        ; Ay * Bz
    movss xmm7, xmm2        ; Az
    mulss xmm7, xmm4        ; Az * By
    subss xmm6, xmm7        ; AyBz - AzBy = Cx
    
    movss xmm7, xmm2        ; Az
    mulss xmm7, xmm3        ; Az * Bx
    movss xmm8, xmm0        ; Ax
    mulss xmm8, xmm5        ; Ax * Bz
    subss xmm7, xmm8        ; AzBx - AxBz = Cy
    
    movss xmm8, xmm0        ; Ax
    mulss xmm8, xmm4        ; Ax * By
    movss xmm9, xmm1        ; Ay
    mulss xmm9, xmm3        ; Ay * Bx
    subss xmm8, xmm9        ; AxBy - AyBx = Cz
    
    ; Store result
    movss [rdx], xmm6       ; Cx
    movss [rdx+4], xmm7     ; Cy
    movss [rdx+8], xmm8     ; Cz
    
    ret

vector_normalize:
    ; Input: RDI = vector, RSI = result
    ; Normalize vector to unit length
    
    movss xmm0, [rdi]       ; x
    movss xmm1, [rdi+4]     ; y
    movss xmm2, [rdi+8]     ; z
    
    ; Calculate length squared
    movss xmm3, xmm0
    mulss xmm3, xmm3        ; x^2
    movss xmm4, xmm1
    mulss xmm4, xmm4        ; y^2
    movss xmm5, xmm2
    mulss xmm5, xmm5        ; z^2
    
    addss xmm3, xmm4        ; x^2 + y^2
    addss xmm3, xmm5        ; x^2 + y^2 + z^2
    
    ; Calculate reciprocal square root (fast approximation)
    rsqrtss xmm6, xmm3      ; 1/sqrt(length^2)
    
    ; Multiply components by reciprocal length
    mulss xmm0, xmm6        ; x * (1/length)
    mulss xmm1, xmm6        ; y * (1/length)
    mulss xmm2, xmm6        ; z * (1/length)
    
    ; Store normalized result
    movss [rsi], xmm0
    movss [rsi+4], xmm1
    movss [rsi+8], xmm2
    
    ret
