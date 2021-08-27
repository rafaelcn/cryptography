#include <iostream>
#include <cstring>
#include <vector>
#include <fstream>
#include <algorithm>
#include <functional>

#include "vigenere/vigenere.hpp"
#include "vigenere/adversary.hpp"

void usage();

const std::string encrypt(const std::string&, const std::string&);
const std::string decrypt(const std::string&, const std::string&);

const std::string open(const std::string&);

int main(int argc, char **argv) {

    if (argc <= 1) {
        usage();
    } else {
        // the first argument would be attack, encrypt or decrypt
        const auto command = std::string(argv[1]);

        if (command == "--help") {
            usage();
        } else if (command == "--attack") {
            if (argc < 3) {
                usage();
                return 0;
            }

            const auto filename = std::string(argv[2]);
            const auto criptogram = open(filename);

            VigenereAdversary va(criptogram);
            auto outcomes = va.attack();

            for (const auto e: outcomes) {
                std::cout << e;
            }
        } else if (command == "--encrypt" || command == "--decrypt") {
            if (argc < 4) {
                usage();
                return 0;
            }

            const auto filename = std::string(argv[2]);
            const auto key = std::string(argv[3]);

            const auto text = open(filename);

            if (command == "--encrypt") {
                std::cout << encrypt(text, key);
            } else {
                std::cout << decrypt(text, key);
            }
        } else {
            usage();
        }
    }

    return 0;
}

void usage() {

    std::cout << "Usage vigenere.exe <option> <arguments>\n\n"
              << ""
              << "--help\n"
              << "--attack  <file>\n"
              << "--encrypt <file> <key>\n"
              << "--decrypt <file> <key>\n"
              << "Examples\n---------\n\n"
              << "vigenere.exe --attack challenges/challenge_1.txt\n"
              << "vigenere.exe --encrypt bin/sample.txt \"SOSECRET\"\n\n"
              << "vigenere.exe --decrypt bin/encrypted.txt \"ARARA\"\n\n"
              << "Works only on latin alphabets as it uses the ASCII to rotate "
              << "characters, I hope you understand. じゃ、また。";
}

const std::string encrypt(const std::string& text, const std::string& key) {

    Vigenere v(key);

    return v.encrypt(text);
}
const std::string decrypt(const std::string& text, const std::string& key) {

    Vigenere v(key);

    return v.decrypt(text);
}

const std::string open(const std::string& filename) {

    std::ifstream file(filename);

    if(!file.is_open()) {
        std::cerr << "error while reading the file " << filename << ". "
                    << "are you sure it does exists?";
    }

    std::string line;
    std::string text;

    while (std::getline(file, line)) {
        std::replace(line.begin(), line.end(), '\n', ' ');
        text += line;
    }

    return text;
}