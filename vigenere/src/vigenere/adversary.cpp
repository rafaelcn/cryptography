#include "adversary.hpp"

#include <map>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <algorithm>

#include "vigenere.hpp"
#include "../utils/magic.hpp"

VigenereAdversary::VigenereAdversary(const std::string& criptogram) {
    m_alphabet = "ABCDEFGHIJKLMNOPQRSTUVXWYZ";
    m_criptogram = criptogram;
}

float VigenereAdversary::get_frequency(const char c, const std::vector<char>& letters) {

    float freq = 0.0f;

    for (const auto l : letters) {
        if (c == l) {
            freq += 1;
        }
    }

    return freq/float(letters.size());
}

void VigenereAdversary::print_graph(const std::map<char, float>& d) {

    auto data = std::map<std::string, float>();

    for (const auto p : d) {
        auto c = std::string(1, p.first);
        data[c] = p.second;
    }

    print_graph(data);
}

void VigenereAdversary::print_graph(const std::map<std::string, float>& d) {

    for (const auto lf : d) {
        std::string bar_size = "";

        for (size_t i = 0; i < std::floor(lf.second*100); i++) {
            if (i % 15 == 0) {
                bar_size += "⊙";
            }
        }

        std::cout << lf.first << " " << bar_size << "\n";
        //std::cout << "[" << lf.second << "]\n";
    }
}

std::string VigenereAdversary::attack() {

    std::string filtered_criptogram;

    // filter the criptogram first to make sure that there are only letters.
    for (auto letter : m_criptogram) {
        if (m_alphabet.find(std::toupper(letter)) != std::string::npos) {
            filtered_criptogram += std::toupper(letter);
        }
    }

    // map how many coincidences there by the step on which it is
    std::map<int, int> coincidences;

    // LVXJSAKGGESLZXFYHZXFX
    //  LVXJSAKGGESLZXFYHZXFX

    size_t step = 1;

    // for up to keys with size 100
    while (step < 100) {
        int j = step;
        for (size_t i = 0; i < filtered_criptogram.size(); i++) {
            if (filtered_criptogram[i] == filtered_criptogram[j]) {
                coincidences[step] += 1;
            }
            j++;
        }
        step++;
    }

    for (auto e : coincidences) {
        std::cout << "coincidences[" << e.first << "] -> " << e.second << "\n";
    }

    size_t key_lenght;
    std::cout << "give a possible key lenght: ";
    std::cin >> key_lenght;

    // found the key length? nice.
    // calculate the letter frequency within the text, but do so with each
    // letter of the key that encoded the text

    // suppose a 3 letter key and the following criptogram
    //
    // LVXJS AK GGESLZXFY HZXFX
    //
    // 12312 12 123123123 12312
    //
    // bucket 1 -> L,J,A,G,S,X,H,F
    // bucket 2 -> V,S,K,G,L,F,Z,X
    // bucket 3 -> X,E,Z,Y,X
    //
    // these bucket letters are displaced (rotated) from their original
    // position, the decoded position. Compare it with the letter frequency of
    // the original language.

    std::map<int, std::vector<char>> bins;

    for (size_t j = 0; j < key_lenght; j++) {
        bins[j] = std::vector<char>();
        for (size_t i = 0; i < filtered_criptogram.size(); i++) {
            // filling in the bins
            if ((i % key_lenght) == j) {
                bins[j].push_back(filtered_criptogram[i]);
            }
        }
    }

#ifdef DEBUG
    for (const auto& b : bins) {
        std::cout << "bin " << b.first << " -> ";
        for (auto e : b.second) {
            std::cout << e << " ";
        }
        std::cout << "\n";
    }
#endif

    // for each bin we have to calculate the letter frequency
    auto bins_frequency = std::vector<std::map<char, float>>();

    for (const auto& bin : bins) {
        auto bin_frequency = std::map<char, float>();
        for (const auto l : bin.second) {
            bin_frequency[l] = VigenereAdversary::get_frequency(l, bin.second);
        }
        bins_frequency.push_back(bin_frequency);
    }

    // guess, for each bin, how many chars it has been rotated, comparing it to
    // the original frequency distribution of the english alphabet

    std::cout << "\nENGLISH LETTER FREQUENCY\n=========================\n";
    print_graph(en_letter_frequency);
    std::cout << "\n";

    std::cout << "\nPORTUGUESE LETTER FREQUENCY\n===========================\n";
    print_graph(pt_letter_frequency);
    std::cout << "\n";

    for (auto bf : bins_frequency) {
        std::cout << "BIN: \n";

        for (auto v : bf) {
            std::cout << v.first << " -> " << v.second << "\n";
        }
        //print_graph(bf);
        std::cout << "\n";
    }

    std::string key = "";

    for (size_t i = 0; i < bins_frequency.size(); i++) {
        std::string c;

        std::cout << "BIN " << i << " ROTATED BY: ";
        std::cin >> c;

        key += c;
    }

    Vigenere v(key);

    return v.decrypt(m_criptogram);
}

