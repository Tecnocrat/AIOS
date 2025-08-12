; kernel_ops.asm - minimal x64 MASM routine for CPUID leaf 0
; Assembler: MASM (ml64) via CMake ASM_MASM

.code

PUBLIC KernelCpuidLeaf0
PUBLIC KernelCpuidLeaf
PUBLIC KernelReadTSC
PUBLIC KernelReadTSCP
PUBLIC KernelSimdAddF32

; ---------------------------------------------------------
; unsigned __int64 KernelCpuidLeaf0();
; Returns: RAX = max basic leaf
; ---------------------------------------------------------
KernelCpuidLeaf0 PROC
    push    rbx
    xor     eax, eax
    xor     ecx, ecx
    cpuid
    ; EAX now holds max basic leaf
    pop     rbx
    ret
KernelCpuidLeaf0 ENDP

; ---------------------------------------------------------
; void KernelCpuidLeaf(unsigned leaf, unsigned subleaf,
;                      unsigned* eax, unsigned* ebx,
;                      unsigned* ecx, unsigned* edx);
; Windows x64 calling: RCX, RDX, R8, R9, stack ...
; RCX=leaf RDX=subleaf R8=ptrEAX R9=ptrEBX [rsp+40]=ptrECX [rsp+48]=ptrEDX
; ---------------------------------------------------------
KernelCpuidLeaf PROC
    push    rbx
    mov     eax, ecx        ; leaf
    mov     ecx, edx        ; subleaf
    cpuid
    ; R8 -> eax*, R9 -> ebx*, [rsp+40] -> ecx*, [rsp+48] -> edx*
    mov     r10, r8
    mov     [r10], eax
    mov     r10, r9
    mov     [r10], ebx
    mov     r10, [rsp+40]
    mov     [r10], ecx
    mov     r10, [rsp+48]
    mov     [r10], edx
    pop     rbx
    ret
KernelCpuidLeaf ENDP

; ---------------------------------------------------------
; unsigned __int64 KernelReadTSC(); (rdtsc, not serialized)
; ---------------------------------------------------------
KernelReadTSC PROC
    rdtsc               ; EDX:EAX
    shl     rdx, 32
    or      rax, rdx
    ret
KernelReadTSC ENDP

; ---------------------------------------------------------
; unsigned __int64 KernelReadTSCP(unsigned *aux); (rdtscp serialized)
; RCX holds pointer to aux (Windows x64)
; ---------------------------------------------------------
KernelReadTSCP PROC
    rdtscp              ; EDX:EAX, ECX=aux
    mov     r8, rcx
    mov     [r8], ecx
    shl     rdx, 32
    or      rax, rdx
    ret
KernelReadTSCP ENDP

; ---------------------------------------------------------
; void KernelSimdAddF32(const float* a, const float* b, float* out, unsigned count);
; RCX=a, RDX=b, R8=out, R9=count
; Processes 4 floats at a time with SSE, remainder scalar.
; ---------------------------------------------------------
KernelSimdAddF32 PROC
    push    rbx
    mov     r10, rcx        ; a
    mov     r11, rdx        ; b
    mov     r12, r8         ; out
    mov     eax, r9d        ; count
    xor     r13d, r13d
    ; Loop over 4-float blocks
    cmp     eax, 4
    jb      simd_tail
simd_loop:
    movups  xmm0, [r10 + r13*4]
    movups  xmm1, [r11 + r13*4]
    addps   xmm0, xmm1
    movups  [r12 + r13*4], xmm0
    add     r13d, 4
    cmp     r13d, eax
    jbe     simd_loop
simd_tail:
    cmp     r13d, eax
    jge     simd_done
tail_loop:
    mov     ebx, [r10 + r13*4]
    mov     edx, [r11 + r13*4]
    add     ebx, edx
    mov     [r12 + r13*4], ebx
    inc     r13d
    cmp     r13d, eax
    jl      tail_loop
simd_done:
    pop     rbx
    ret
KernelSimdAddF32 ENDP

END
