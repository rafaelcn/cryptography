#ifndef VIGENERE_HPP
#define VIGENERE_HPP

#include <string>

class Vigenere {
private:
    std::string m_alphabet;
    std::string m_key;

    // Direction encapsulates the direction that the algorithm will rotate the
    // characters respective to the alphabet. This conception is, clearly,
    // something from languages that are read and written left to right.
    enum Direction {
        LEFT,
        RIGHT
    };

    std::string rotate(const std::string&, const Direction direction);
public:
    Vigenere(const std::string& key);
    Vigenere(const std::string& alphabet, const std::string& key);
    ~Vigenere() {}

    std::string encrypt(const std::string&);
    std::string decrypt(const std::string&);
};

#endif // VIGENERE_HPP