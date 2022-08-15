FROM        ubuntu:20.04 AS base

WORKDIR     /tmp/workdir

RUN     apt-get -yqq update && \
        apt-get install -yq --no-install-recommends pip python3-pandas python3-sklearn wget unzip && \
        apt-get autoremove -y && \
        apt-get clean -y && \
        pip install xgboost==0.90
RUN     mkdir /root/ImmunIC && \
        cd /root/ImmunIC && \
        wget https://github.com/hayounlee-lab/ImmunIC/archive/refs/heads/main.zip && \
        unzip -j main.zip

ENTRYPOINT ["/bin/bash", "/root/ImmunIC/runImmunIC.bash"]
