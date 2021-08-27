#ifndef ADVERSARY_HPP
#define ADVERSARY_HPP

#include <map>
#include <string>
#include <vector>

class VigenereAdversary {
private:
    std::string m_alphabet;
    std::string m_criptogram;

    float get_frequency(const char, const std::vector<char>&);

    void print_graph(const std::map<char, float>&);
    void print_graph(const std::map<std::string, float>&);

public:
    VigenereAdversary(const std::string& criptogram);
    ~VigenereAdversary() {}

    std::string attack();
};

#endif // ADVERSARY_HPP