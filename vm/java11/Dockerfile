FROM gradle:6.9-jdk11

RUN apt update && apt install -y debian-keyring debian-archive-keyring
RUN apt-key update \
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 04EE7237B7D453EC \
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 0E98404D386FA1D9 \
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 605C66F00D6C9793

RUN echo deb http://ftp.debian.org/debian bullseye main contrib >> /etc/apt/sources.list
RUN apt update && apt install -y pup

WORKDIR /environment
ENV GRADLE_USER_HOME=/environment/.gradle

COPY build.gradle .
RUN gradle resolveDependencies --no-daemon --refresh-dependencies

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# RUN useradd judge
# USER judge

CMD ./entrypoint.sh
