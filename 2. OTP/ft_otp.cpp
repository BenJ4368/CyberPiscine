#include <iostream>
#include <fstream>
#include <iomanip>
#include <openssl/hmac.h>
#include <openssl/evp.h>
#include <openssl/rand.h>
#include <cstring>
#include <ctime>
#include <vector>
#include <sstream>
#include <filesystem>

const std::string KEY_FILE = "ft_otp.key";
const size_t KEY_LENGTH = 64;

void saveKey(const std::string &hexKey) {
    if (hexKey.size() < KEY_LENGTH)
        throw std::invalid_argument("The key must be at least 64 characters long.");

    // Convert hex to raw bytes
    std::vector<unsigned char> key(hexKey.size() / 2); // 2 hex characters = 1 byte
    for (size_t i = 0; i < hexKey.size(); i += 2)
        key[i / 2] = std::stoi(hexKey.substr(i, 2), nullptr, 16);

    // Encrypt the key (XOR)
    // Simple encryption method to prevent the key from being stored in plain text (better than nothing)
    unsigned char xorKey = 0xAA;  // XOR key
    for (auto &byte : key)
        byte ^= xorKey; // ^= is the XOR operator

    // Save encrypted key to file
    std::ofstream outFile(KEY_FILE, std::ios::binary); // Opening KEY_FILE in binary mode, so no interpretation of characters.
    if (!outFile)
        throw std::runtime_error("Failed to open key file for writing.");
    outFile.write(reinterpret_cast<const char *>(key.data()), key.size());
    outFile.close();
    std::cout << "Encrypted key saved to " << KEY_FILE << std::endl;
}

std::vector<unsigned char> loadKey() {
    // Read encrypted key from file
    if (!std::filesystem::exists(KEY_FILE))
        throw std::runtime_error("Key file does not exist. Use -g to generate one first.");

    std::ifstream inFile(KEY_FILE, std::ios::binary | std::ios::ate); // Open binary file, cursor at the end ('ate')
    if (!inFile)
        throw std::runtime_error("Failed to open key file for reading.");

    std::streamsize size = inFile.tellg(); // File size. tellg() returns the position of the cursor (we used 'ate')
    inFile.seekg(0, std::ios::beg); // Move cursor to the beginning again.

    std::vector<unsigned char> key(size);
    if (!inFile.read(reinterpret_cast<char *>(key.data()), size)) // Read the key into the vector 'key'
        throw std::runtime_error("Failed to read key from file.");
    inFile.close();

    // Decrypt the key, same XOR operation
    unsigned char xorKey = 0xAA;
    for (auto &byte : key)
        byte ^= xorKey;

    return key;
}

std::vector<unsigned char> prepareKey(const std::vector<unsigned char>& key) {
    const size_t blockSize = 64; // SHA1 block size

    std::vector<unsigned char> K(blockSize, 0x00); // init 64 bytes to 0
    if (key.size() > blockSize) {
        // Hash the key if it's too long
        unsigned char hashed[EVP_MAX_MD_SIZE];
        unsigned int hashLen;
        EVP_Digest(key.data(), key.size(), hashed, &hashLen, EVP_sha1(), nullptr);
        std::copy(hashed, hashed + hashLen, K.begin());
    } else {
        std::copy(key.begin(), key.end(), K.begin());
    }
    return K;
}

std::vector<unsigned char> computeHMAC_SHA1(const std::vector<unsigned char>& key, const unsigned char* message, size_t messageLen) {
    const size_t blockSize = 64;
    auto K = prepareKey(key);

    // ipad et opad
    std::vector<unsigned char> o_key_pad(blockSize);
    std::vector<unsigned char> i_key_pad(blockSize);

    for (size_t i = 0; i < blockSize; ++i) {
        o_key_pad[i] = K[i] ^ 0x5c;
        i_key_pad[i] = K[i] ^ 0x36;
    }

    // 1. H(i_key_pad || message)
    std::vector<unsigned char> inner(i_key_pad.begin(), i_key_pad.end());
    inner.insert(inner.end(), message, message + messageLen);

    unsigned char innerHash[EVP_MAX_MD_SIZE];
    unsigned int innerHashLen;
    EVP_Digest(inner.data(), inner.size(), innerHash, &innerHashLen, EVP_sha1(), nullptr);

    // 2. H(o_key_pad || innerHash)
    std::vector<unsigned char> outer(o_key_pad.begin(), o_key_pad.end());
    outer.insert(outer.end(), innerHash, innerHash + innerHashLen);

    unsigned char finalHash[EVP_MAX_MD_SIZE];
    unsigned int finalHashLen;
    EVP_Digest(outer.data(), outer.size(), finalHash, &finalHashLen, EVP_sha1(), nullptr);

    return std::vector<unsigned char>(finalHash, finalHash + finalHashLen); // 20 bytes
}


std::string generateHOTP(const std::vector<unsigned char> &key, uint64_t counter) {
    // Convert counter to bytes (big-endian)
    // Extracting bytes from the end of the 64-bit integer makes it easier to handle.
    unsigned char counterBytes[8];
    for (int i = 7; i >= 0; --i) {
        counterBytes[i] = counter & 0xFF;
        counter >>= 8;
    }

    // Generate HMAC-SHA1
    std::vector<unsigned char> hmacVec = computeHMAC_SHA1(key, counterBytes, 8);
    unsigned char* hmacResult = hmacVec.data();
    unsigned int resultLen = hmacVec.size();

    // Truncate (Dynamic Truncation)
    int offset = hmacResult[resultLen - 1] & 0x0F;
    // Last 4 bits of the last byte, exemple:
    // lastbyte = 1010 1101
    // 0x0F     = 0000 1111   apply binary mask
    // & result = 0000 1101   only 4 last bits are kept
    // offset = 0000 1101 = 13. This is the index where the 4 bytes will be extracted from the hash.
    // guaranties that the offset is between 0 and 15, and random-ish.

    uint32_t truncatedHash = 0;
    for (int i = 0; i < 4; ++i) { // Getting 4 bytes from the hash, starting at the offset.
        truncatedHash <<= 8;
        truncatedHash |= hmacResult[offset + i];
    }
    truncatedHash &= 0x7FFFFFFF;  // Ignore the sign bit (using binary mask again)
    truncatedHash %= 1000000;    // Limit to 6 digits

    // Format the OTP as a 6-digit string (fill with zeros if needed)
    std::ostringstream otpStream;
    otpStream << std::setw(6) << std::setfill('0') << truncatedHash;
    return otpStream.str();
}

void generateAndPrintOTP() {
    auto key = loadKey();

    uint64_t counter = std::time(nullptr) / 30; // Epoch time, 30 seconds interval.

    std::string otp = generateHOTP(key, counter);
    std::cout << "Your OTP is: " << otp << std::endl;
}

int main(int argc, char *argv[]) {
    try {
        if (argc < 2)
            throw std::runtime_error("Usage: ft_otp <file>");
        
        std::string option = argv[1];
        if (option == "-g") {
            if (argc != 3)
                throw std::invalid_argument("Usage: ft_otp -g <key>");

            std::string hexKey = argv[2];
            saveKey(hexKey);
        } else if (option == "-k")
            generateAndPrintOTP();
        else
            throw std::invalid_argument("Invalid option. Use -g to generate a key or -k to generate an OTP.");
    } catch (const std::exception &e) {
        std::cerr << "Error: " << e.what() << std::endl;
         return 1;
    }
}