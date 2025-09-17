; AIOS Emoticon Destroyer - x86-64 Assembly Implementation  
; STRICT NO EMOTICON POLICY ENFORCED
; High-performance emoticon detection and removal at machine level

.data
    ; File handling
    filename       db 260 dup(0)      ; MAX_PATH buffer
    file_handle    dq 0
    file_size      dq 0
    bytes_read     dq 0
    bytes_written  dq 0
    
    ; Buffer management
    buffer         db 1048576 dup(0)  ; 1MB buffer
    clean_buffer   db 1048576 dup(0)  ; Clean output buffer
    
    ; Statistics
    files_processed     dq 0
    emoticons_destroyed dq 0
    backup_files_created dq 0
    
    ; String constants
    msg_header     db '[AIOS] Emoticon Destroyer Assembly Engine', 0Dh, 0Ah, 0
    msg_policy     db '[POLICY] No emoticons allowed in codebase', 0Dh, 0Ah, 0
    msg_processing db '[ASM] Processing: ', 0
    msg_success    db '[SUCCESS] Removed ', 0
    msg_emoticons  db ' emoticons from: ', 0
    msg_error      db '[ERROR] ', 0
    msg_stats      db 0Dh, 0Ah, '[STATISTICS]', 0Dh, 0Ah, 0
    msg_files      db 'Files processed: ', 0
    msg_destroyed  db 'Emoticons destroyed: ', 0
    msg_backups    db 'Backup files created: ', 0
    newline        db 0Dh, 0Ah, 0
    
    ; Emoticon patterns (simplified for assembly)
    ; UTF-8 byte patterns for common emoticons
    emoticon_patterns:
        ; Smiling face (U+1F600 = F0 9F 98 80)
        db 0F0h, 09Fh, 098h, 080h
        ; Grinning face (U+1F601 = F0 9F 98 81) 
        db 0F0h, 09Fh, 098h, 081h
        ; Face with tears (U+1F602 = F0 9F 98 82)
        db 0F0h, 09Fh, 098h, 082h
        ; Smiling face with open mouth (U+1F603 = F0 9F 98 83)
        db 0F0h, 09Fh, 098h, 083h
        ; Smiling face with open mouth and smiling eyes (U+1F604 = F0 9F 98 84)
        db 0F0h, 09Fh, 098h, 084h
        ; Smiling face with open mouth and cold sweat (U+1F605 = F0 9F 98 85)
        db 0F0h, 09Fh, 098h, 085h
        ; Winking face (U+1F609 = F0 9F 98 89)
        db 0F0h, 09Fh, 098h, 089h
        ; Heart eyes (U+1F60D = F0 9F 98 8D)
        db 0F0h, 09Fh, 098h, 08Dh
        ; Thinking face (U+1F914 = F0 9F A4 94)
        db 0F0h, 09Fh, 0A4h, 094h
        ; Thumbs up (U+1F44D = F0 9F 91 8D)
        db 0F0h, 09Fh, 091h, 08Dh
        
    pattern_count  equ 10
    pattern_size   equ 4
    
    ; ASCII emoticon patterns
    ascii_emoticons:
        db ':)', 0, 0   ; Pad to 4 bytes
        db ':(', 0, 0
        db ':D', 0, 0
        db ';)', 0, 0
        db ':P', 0, 0
        db 'XD', 0, 0
        db '8)', 0, 0
        db ':(', 0, 0
        db ':o', 0, 0
        db ':|', 0, 0
        
    ascii_pattern_count equ 10

.code
main proc
    ; Initialize
    call print_header
    
    ; Get command line arguments
    call get_command_line_args
    test rax, rax
    jz exit_error
    
    ; Process the target file/directory
    mov rcx, offset filename
    call process_target
    
    ; Print statistics
    call print_statistics
    
    ; Exit successfully
    mov rcx, 0
    call ExitProcess

exit_error:
    mov rcx, 1
    call ExitProcess
main endp

print_header proc
    mov rcx, offset msg_header
    call print_string
    mov rcx, offset msg_policy
    call print_string
    ret
print_header endp

get_command_line_args proc
    ; Get command line
    call GetCommandLineA
    mov rsi, rax
    
    ; Skip program name
    call skip_program_name
    
    ; Copy filename
    mov rdi, offset filename
    mov rcx, 260
    call copy_filename
    
    ; Check if filename was provided
    mov al, byte ptr [filename]
    test al, al
    jz no_filename
    
    mov rax, 1
    ret

no_filename:
    mov rcx, offset msg_error
    call print_string
    mov rcx, offset filename
    mov byte ptr [rcx], 'N'
    mov byte ptr [rcx+1], 'o'
    mov byte ptr [rcx+2], ' '
    mov byte ptr [rcx+3], 'f'
    mov byte ptr [rcx+4], 'i'
    mov byte ptr [rcx+5], 'l'
    mov byte ptr [rcx+6], 'e'
    mov byte ptr [rcx+7], 0
    call print_string
    xor rax, rax
    ret
get_command_line_args endp

skip_program_name proc
    ; Skip until space or quote end
skip_loop:
    lodsb
    test al, al
    jz skip_done
    cmp al, ' '
    je skip_spaces
    cmp al, '"'
    je skip_quote
    jmp skip_loop

skip_quote:
    lodsb
    test al, al
    jz skip_done
    cmp al, '"'
    jne skip_quote
    jmp skip_spaces

skip_spaces:
    lodsb
    test al, al
    jz skip_done
    cmp al, ' '
    je skip_spaces
    dec rsi

skip_done:
    ret
skip_program_name endp

copy_filename proc
    ; Copy filename from command line
copy_loop:
    lodsb
    test al, al
    jz copy_done
    cmp al, ' '
    je copy_done
    stosb
    loop copy_loop

copy_done:
    mov al, 0
    stosb
    ret
copy_filename endp

process_target proc
    ; rcx = filename
    push rcx
    
    ; Print processing message
    mov rcx, offset msg_processing
    call print_string
    pop rcx
    push rcx
    call print_string
    mov rcx, offset newline
    call print_string
    
    ; Open file
    pop rcx
    call open_file
    test rax, rax
    jz process_error
    mov file_handle, rax
    
    ; Get file size
    mov rcx, file_handle
    call get_file_size
    mov file_size, rax
    
    ; Read file content
    call read_file_content
    test rax, rax
    jz process_error
    
    ; Process emoticons
    call process_emoticons
    
    ; Write cleaned content back
    call write_file_content
    
    ; Close file
    mov rcx, file_handle
    call CloseHandle
    
    ; Update statistics
    inc files_processed
    
    mov rax, 1
    ret

process_error:
    xor rax, rax
    ret
process_target endp

open_file proc
    ; rcx = filename
    mov rdx, GENERIC_READ or GENERIC_WRITE
    mov r8, FILE_SHARE_READ
    mov r9, 0  ; No security attributes
    push OPEN_EXISTING
    push FILE_ATTRIBUTE_NORMAL
    push 0     ; No template
    call CreateFileA
    add rsp, 24
    
    cmp rax, INVALID_HANDLE_VALUE
    je open_failed
    ret

open_failed:
    xor rax, rax
    ret
open_file endp

get_file_size proc
    ; rcx = file handle
    push 0
    mov rdx, rsp
    call GetFileSizeEx
    pop rax
    ret
get_file_size endp

read_file_content proc
    mov rcx, file_handle
    mov rdx, offset buffer
    mov r8, file_size
    cmp r8, 1048576
    jb read_size_ok
    mov r8, 1048576

read_size_ok:
    push 0
    mov r9, rsp
    push 0
    call ReadFile
    add rsp, 16
    
    test rax, rax
    jz read_failed
    mov rax, 1
    ret

read_failed:
    xor rax, rax
    ret
read_file_content endp

process_emoticons proc
    ; Process buffer for emoticon removal
    mov rsi, offset buffer        ; Source
    mov rdi, offset clean_buffer  ; Destination
    mov rcx, file_size           ; Size to process
    xor r8, r8                   ; Emoticon count
    
process_loop:
    test rcx, rcx
    jz process_done
    
    ; Check for UTF-8 emoticon patterns
    call check_utf8_emoticon
    test rax, rax
    jnz found_utf8_emoticon
    
    ; Check for ASCII emoticon patterns
    call check_ascii_emoticon
    test rax, rax
    jnz found_ascii_emoticon
    
    ; Regular character - copy it
    lodsb
    stosb
    dec rcx
    jmp process_loop

found_utf8_emoticon:
    ; Skip UTF-8 emoticon (4 bytes)
    add rsi, 4
    sub rcx, 4
    inc r8
    jmp process_loop

found_ascii_emoticon:
    ; Skip ASCII emoticon (variable length in rax)
    add rsi, rax
    sub rcx, rax
    inc r8
    jmp process_loop

process_done:
    ; Store null terminator
    mov al, 0
    stosb
    
    ; Update emoticon count
    add emoticons_destroyed, r8
    
    ; Calculate new file size
    mov rax, rdi
    sub rax, offset clean_buffer
    mov file_size, rax
    
    ret
process_emoticons endp

check_utf8_emoticon proc
    ; Check if current position matches UTF-8 emoticon pattern
    push rcx
    push rsi
    
    mov rbx, offset emoticon_patterns
    mov rdx, pattern_count
    
check_utf8_loop:
    test rdx, rdx
    jz no_utf8_match
    
    ; Compare 4 bytes
    mov eax, dword ptr [rsi]
    cmp eax, dword ptr [rbx]
    je utf8_match_found
    
    add rbx, pattern_size
    dec rdx
    jmp check_utf8_loop

utf8_match_found:
    pop rsi
    pop rcx
    mov rax, 1
    ret

no_utf8_match:
    pop rsi
    pop rcx
    xor rax, rax
    ret
check_utf8_emoticon endp

check_ascii_emoticon proc
    ; Check for ASCII emoticon patterns
    push rcx
    push rsi
    
    mov rbx, offset ascii_emoticons
    mov rdx, ascii_pattern_count
    
check_ascii_loop:
    test rdx, rdx
    jz no_ascii_match
    
    ; Compare first 2 characters
    mov ax, word ptr [rsi]
    cmp ax, word ptr [rbx]
    je ascii_match_found
    
    add rbx, 4  ; Each pattern is 4 bytes (padded)
    dec rdx
    jmp check_ascii_loop

ascii_match_found:
    pop rsi
    pop rcx
    mov rax, 2  ; ASCII emoticons are 2 characters
    ret

no_ascii_match:
    pop rsi
    pop rcx
    xor rax, rax
    ret
check_ascii_emoticon endp

write_file_content proc
    ; Set file pointer to beginning
    mov rcx, file_handle
    mov rdx, 0
    mov r8, 0
    mov r9, FILE_BEGIN
    call SetFilePointer
    
    ; Write cleaned content
    mov rcx, file_handle
    mov rdx, offset clean_buffer
    mov r8, file_size
    push 0
    mov r9, rsp
    push 0
    call WriteFile
    add rsp, 16
    
    ; Truncate file at current position
    mov rcx, file_handle
    call SetEndOfFile
    
    ret
write_file_content endp

print_statistics proc
    mov rcx, offset msg_stats
    call print_string
    
    mov rcx, offset msg_files
    call print_string
    mov rax, files_processed
    call print_number
    mov rcx, offset newline
    call print_string
    
    mov rcx, offset msg_destroyed
    call print_string
    mov rax, emoticons_destroyed
    call print_number
    mov rcx, offset newline
    call print_string
    
    ret
print_statistics endp

print_string proc
    ; rcx = string pointer
    push rcx
    call lstrlenA
    mov r8, rax
    pop rdx
    
    mov rcx, STD_OUTPUT_HANDLE
    call GetStdHandle
    mov rcx, rax
    
    push 0
    mov r9, rsp
    push 0
    call WriteConsoleA
    add rsp, 16
    
    ret
print_string endp

print_number proc
    ; rax = number to print
    push rbp
    mov rbp, rsp
    sub rsp, 32
    
    ; Convert number to string
    mov rbx, 10
    mov rcx, rsp
    add rcx, 31
    mov byte ptr [rcx], 0
    
convert_loop:
    dec rcx
    xor rdx, rdx
    div rbx
    add dl, '0'
    mov byte ptr [rcx], dl
    test rax, rax
    jnz convert_loop
    
    ; Print the string
    push rcx
    call print_string
    add rsp, 8
    
    add rsp, 32
    pop rbp
    ret
print_number endp

; Constants
GENERIC_READ         equ 80000000h
GENERIC_WRITE        equ 40000000h
FILE_SHARE_READ      equ 1
OPEN_EXISTING        equ 3
FILE_ATTRIBUTE_NORMAL equ 80h
INVALID_HANDLE_VALUE equ -1
FILE_BEGIN           equ 0
STD_OUTPUT_HANDLE    equ -11

; External functions
extern GetCommandLineA: proc
extern CreateFileA: proc
extern CloseHandle: proc
extern GetFileSizeEx: proc
extern ReadFile: proc
extern WriteFile: proc
extern SetFilePointer: proc
extern SetEndOfFile: proc
extern GetStdHandle: proc
extern WriteConsoleA: proc
extern lstrlenA: proc
extern ExitProcess: proc

end