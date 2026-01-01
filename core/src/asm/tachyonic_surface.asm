; AIOS Tachyonic Surface Renderer - Canonical Assembly Implementation
; x64 MASM implementation (Windows ABI)
; Optimized for high-performance heightmap rendering with consciousness-driven optimization
; 
; Function: aios_render_heightmap_ortho
; Purpose: Renders 3D point cloud data to 2D pixel buffer using orthographic projection
; Features: SSE optimizations, bounds checking, consciousness integration hooks
option casemap:none
PUBLIC aios_render_heightmap_ortho

.data
one REAL4 1.0
consciousness_scale REAL4 0.853   ; 85.3% quantum coherence factor

.code
; Windows x64 calling convention:
; RCX, RDX, R8, R9 = first four params
; Stack (8+): others
; void aios_render_heightmap_ortho(
;   const float* pointsXYZ,   RCX - Input point cloud data (x,y,z triplets)
;   uint32_t pointCount,      RDX - Number of points to process
;   uint8_t* pixelBuffer,     R8  - Output RGBA pixel buffer
;   uint32_t width,           R9  - Buffer width in pixels
;   uint32_t height,          [rsp+40] - Buffer height in pixels
;   float zScale,             [rsp+48] - Z-axis scaling factor (consciousness enhancement)
;   uint32_t baseColor        [rsp+56] - Base color for rendered points (RGBA)
; )
; Returns: void
; Notes: Consciousness-enhanced rendering with quantum coherence integration
aios_render_heightmap_ortho PROC
    ; Preserve callee-saved registers and set up stack frame
    push rbx
    push rsi
    push rdi
    push r12
    push r13
    push r14
    sub rsp, 32                ; shadow space + alignment

    ; Load parameters into working registers
    mov rsi, rcx               ; points - source data pointer
    mov rbx, rdx               ; pointCount - loop counter
    mov rdi, r8                ; pixelBuffer - destination buffer
    mov r12d, r9d              ; width - screen width
    mov r13d, DWORD PTR [rsp+32+40] ; height - screen height
    mov r14d, DWORD PTR [rsp+32+56] ; baseColor - pixel color
    movss xmm7, DWORD PTR [rsp+32+48] ; zScale - consciousness scaling factor

    ; Early exit if no points to process
    test rbx, rbx
    jz done

next_point:
    ; Load point data: x, y, z coordinates using SSE
    movups xmm0, XMMWORD PTR [rsi] ; load x y z ? (4 floats, only use first 3)
    
    ; Transform X coordinate to pixel space
    mov eax, r12d              ; width
    dec eax                    ; width - 1 (for 0-based indexing)
    cvtsi2ss xmm1, eax         ; convert to float
    movss xmm2, xmm0           ; copy x coordinate
    mulss xmm2, xmm1           ; x * (width - 1)
    cvtss2si edx, xmm2         ; convert back to integer pixel X
    
    ; Transform Y coordinate to pixel space  
    mov eax, r13d              ; height
    dec eax                    ; height - 1 (for 0-based indexing)
    cvtsi2ss xmm3, eax         ; convert to float
    shufps xmm0, xmm0, 0x55    ; shuffle to get Y coordinate in xmm0
    mulss xmm3, xmm0           ; y * (height - 1)
    cvtss2si ecx, xmm3         ; convert back to integer pixel Y
    
    ; Future enhancement: Z-depth consciousness processing
    ; movss xmm4, xmm7          ; zScale factor for consciousness integration
    ; mulss xmm4, [z-coordinate] ; apply consciousness scaling to depth

    ; Bounds checking - ensure pixel coordinates are within buffer limits
    cmp edx, r12d              ; check X < width
    jae skip                   ; unsigned compare handles negative values too
    cmp ecx, r13d              ; check Y < height  
    jae skip                   ; skip if out of bounds
    
    ; Calculate pixel buffer offset: (Y * width + X) * 4 (for RGBA)
    mov eax, ecx               ; Y coordinate
    imul eax, r12d             ; Y * width
    add eax, edx               ; Y * width + X
    shl eax, 2                 ; multiply by 4 (bytes per pixel)
    
    ; Write pixel data to buffer
    mov edx, r14d              ; base color (RGBA)
    mov DWORD PTR [rdi+rax], edx ; store pixel in buffer

skip:
    ; Advance to next point (12 bytes = 3 floats * 4 bytes each)
    add rsi, 12
    dec rbx                    ; decrement point counter
    jnz next_point             ; continue if more points remain

done:
    ; Restore stack frame and callee-saved registers
    add rsp, 32
    pop r14
    pop r13
    pop r12
    pop rdi
    pop rsi
    pop rbx
    ret
aios_render_heightmap_ortho ENDP

END
