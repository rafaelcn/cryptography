#include "vigenere.hpp"

#include <iostream>

#include "../utils/mod.hpp"

Vigenere::Vigenere(const std::string& key) {
    m_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    m_key = key;
}

Vigenere::Vigenere(const std::string& alphabet, const std::string& key) {
    m_alphabet = alphabet;
    m_key = key;
}

std::string Vigenere::encrypt(const std::string& message) {
    return rotate(message, Direction::RIGHT);
}

std::string Vigenere::decrypt(const std::string& criptogram) {
    return rotate(criptogram, Direction::LEFT);
}

std::string Vigenere::rotate(const std::string& message, const Direction dir) {

    std::string rotated = "";

    // key -> SOSECRETHEH
    // rafael é um cara muito lindo não é mesmo
    // SOSECR E TH EHSO SOSEC RETHE HSO S ECRET

    for (size_t i = 0, j = 0; i < message.size(); i++) {
        if (m_alphabet.find(std::toupper(message[i])) != std::string::npos) {
            // find the position of both the message and key chars in the
            // alphabet
            auto kc = m_alphabet.find(std::toupper(m_key[j % m_key.size()]));
            auto cp = m_alphabet.find(std::toupper(message[i]));

            auto ci = 0;

            if (dir == Direction::RIGHT) {
                ci = mod(cp + kc, m_alphabet.size());
            } else {
                ci = mod(cp - kc, m_alphabet.size());
            }

            // I already have the rotated char in the m_alphabet position,
            // now I have to translate it back to a printable character.
            rotated += m_alphabet.at(ci);
            j++;
#ifdef DEBUG
            std::cout << m_alphabet.at(cp) << "[" << cp <<  "]" << " [kc:"
                      << m_alphabet.at(kc) << ", kp:" << kc << "] -> "
                      << m_alphabet.at(ci) << "\n";
#endif // DEBUG
        } else {
            rotated += message[i];
        }
    }

    return rotated;
}