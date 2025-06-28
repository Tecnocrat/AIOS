/*
 * MathConstants: Common mathematical constants for AIOS
 */
#pragma once

#ifndef AIOS_MATH_CONSTANTS_HPP
#define AIOS_MATH_CONSTANTS_HPP

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

#ifndef M_E
#define M_E 2.71828182845904523536
#endif

#ifndef M_SQRT2
#define M_SQRT2 1.41421356237309504880
#endif

// Quantum and physics constants (with proper guards)
#ifndef AIOS_PLANCK_CONSTANT
#define AIOS_PLANCK_CONSTANT 6.62607015e-34  // J⋅Hz⁻¹
#endif

#ifndef AIOS_HBAR
#define AIOS_HBAR 1.054571817e-34            // ℏ = h/(2π)
#endif

#ifndef AIOS_SPEED_OF_LIGHT  
#define AIOS_SPEED_OF_LIGHT 299792458.0      // m/s
#endif

#ifndef AIOS_ELEMENTARY_CHARGE
#define AIOS_ELEMENTARY_CHARGE 1.602176634e-19 // C
#endif

#ifndef AIOS_BOLTZMANN_CONSTANT
#define AIOS_BOLTZMANN_CONSTANT 1.380649e-23 // J/K
#endif

#endif // AIOS_MATH_CONSTANTS_HPP
