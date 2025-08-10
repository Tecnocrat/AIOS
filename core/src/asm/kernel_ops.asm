; kernel_ops.asm - minimal x64 MASM routine for CPUID leaf 0
; Assembler: MASM (ml64) via CMake ASM_MASM

.code

PUBLIC KernelCpuidLeaf0
KernelCpuidLeaf0 PROC
    ; Preserve registers we touch
    push    rbx
    xor     eax, eax        ; leaf 0
    cpuid                   ; EAX=0 => vendor string in EBX,EDX,ECX
    ; Return EAX in RAX, pointer to vendor into RBX/RCX/RDX not returned here
    ; Just restore and return; caller can call extended version if needed.
    pop     rbx
    ret
KernelCpuidLeaf0 ENDP

END
