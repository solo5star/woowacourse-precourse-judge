FROM gradle:6.9-jdk11

RUN apt update && apt install -y libxml2-utils

WORKDIR /environment
ENV GRADLE_USER_HOME=/environment/.gradle

COPY environment/build.gradle .
RUN gradle resolveDependencies --no-daemon --refresh-dependencies

COPY environment/ .
RUN chmod +x entrypoint.sh

# RUN useradd judge
# USER judge

CMD ./entrypoint.sh
