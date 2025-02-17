FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev

COPY stockholm.cpp .
COPY stockholm_script.sh .


RUN g++ -o stockholm stockholm.cpp -lssl -lcrypto -std=c++17 && \
    rm stockholm.cpp && \
    chmod +x stockholm_script.sh && \
    ./stockholm_script.sh && \
    rm stockholm_script.sh

CMD ["/bin/bash"]