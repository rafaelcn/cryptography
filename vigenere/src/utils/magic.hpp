#ifndef MAGIC_HPP
#define MAGIC_HPP

#include <map>
#include <string>

/**
 * This file contains some magic tables that maps a word in the source idiom to
 * a specific probability.
 */

static std::map<std::string, float> en_letter_frequency = {
    {"A", 8.12f },
    {"B", 1.49f },
    {"C", 2.71f },
    {"D", 4.32f },
    {"E", 12.02f },
    {"F", 2.30f },
    {"G", 02.03f },
    {"H", 5.92f },
    {"I", 7.31f },
    {"J", 0.10f },
    {"K", 0.69f },
    {"L", 3.98f },
    {"M", 2.61f },
    {"N", 6.95f },
    {"O", 7.68f },
    {"P", 1.82f },
    {"Q", 0.11f },
    {"R", 06.02f },
    {"S", 6.28f },
    {"T", 9.10f },
    {"U", 2.88f },
    {"V", 1.11f },
    {"W", 02.09f },
    {"X", 0.17f },
    {"Y", 2.11f },
    {"Z", 0.07f }
};

static std::map<std::string, float> pt_letter_frequency = {
    {"A", 12.21f },
    {"B", 1.01f },
    {"C", 3.35f },
    {"D", 4.21f },
    {"E", 13.19f },
    {"F", 1.07f },
    {"G", 1.08f },
    {"H", 1.22f },
    {"I", 5.49f },
    {"J", 0.30f },
    {"K", 0.13f },
    {"L", 3.00f },
    {"M", 5.07f },
    {"N", 5.02f },
    {"O", 10.22f },
    {"P", 3.01f },
    {"Q", 1.10f },
    {"R", 6.73f },
    {"S", 7.35f },
    {"T", 5.07f },
    {"U", 4.46f },
    {"V", 1.72f },
    {"W", 0.05f },
    {"X", 0.28f },
    {"Y", 0.04f },
    {"Z", 0.45f }
};

#endif // MAGIC_HPP