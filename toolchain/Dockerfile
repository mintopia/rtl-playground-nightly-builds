# Built with upstream's checkout as context, on top of upstream's own Dockerfile (tagged rtlplayground-base).
FROM rtlplayground-base
ARG SDCC_TOOLCHAIN
COPY sdcc /tmp/sdcc
RUN sh /tmp/sdcc/build.sh /opt/toolchain/${SDCC_TOOLCHAIN} && rm -rf /tmp/sdcc
# --system: Actions container jobs override HOME, so --global config is ignored
RUN git config --system --add safe.directory '*'
