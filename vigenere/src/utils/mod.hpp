#ifndef MOD_HPP
#define MOD_HPP


/**
 * @brief A mod operator function that works for negative values as the C++ "%"
 * operator is just a division remainder operator.
 */
long mod(long a, long b) {
    return (a%b+b)%b;
}

#endif // MOD_HPP