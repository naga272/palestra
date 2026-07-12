#include <stdio.h>
#include <stdint.h>

void check_simd_support() {
    unsigned int eax, ebx, ecx, edx;

    // Function 1: processor info and feature bits
    eax = 1;
    __asm__ __volatile__ (
        "cpuid"
        : "=a"(eax), "=b"(ebx), "=c"(ecx), "=d"(edx)
        : "a"(eax)
    );

    printf("SIMD extensions supported:\n");

    if (edx & (1 << 25)) printf(" - SSE\n");
    if (edx & (1 << 26)) printf(" - SSE2\n");
    if (ecx & (1 << 0))  printf(" - SSE3\n");
    if (ecx & (1 << 9))  printf(" - SSSE3\n");
    if (ecx & (1 << 19)) printf(" - SSE4.1\n");
    if (ecx & (1 << 20)) printf(" - SSE4.2\n");
    if (ecx & (1 << 28)) printf(" - AVX\n");

    // Serve vedere se AVX è effettivamente utilizzabile (OS supporto + XSAVE)
    if ((ecx & (1 << 27)) && (ecx & (1 << 28))) {
        unsigned int xcr0_eax, xcr0_edx;

        // Leggi il registro XCR0 (controlla che l’OS supporti AVX)
        __asm__ __volatile__ (
            "xgetbv"
            : "=a"(xcr0_eax), "=d"(xcr0_edx)
            : "c"(0)
        );

        if ((xcr0_eax & 0x6) == 0x6) {
            printf("   -> AVX usable (OS supports XSAVE)\n");
        } else {
            printf("   -> AVX present but unusable (OS doesn't support XSAVE)\n");
        }
    }

    // Funzione 7: estensioni avanzate (es. AVX2, AVX-512, BMI, ecc.)
    eax = 7;
    ecx = 0;
    __asm__ __volatile__ (
        "cpuid"
        : "=a"(eax), "=b"(ebx), "=c"(ecx), "=d"(edx)
        : "a"(eax), "c"(ecx)
    );

    if (ebx & (1 << 5))   printf(" - AVX2\n");
    if (ebx & (1 << 16))  printf(" - AVX512F (Foundation)\n");
    if (ebx & (1 << 17))  printf(" - AVX512DQ\n");
    if (ebx & (1 << 28))  printf(" - AVX512CD\n");
    if (ebx & (1 << 30))  printf(" - AVX512BW\n");
    if (ebx & (1 << 31))  printf(" - AVX512VL\n");
}

int main() {
    check_simd_support();
    return 0;
}