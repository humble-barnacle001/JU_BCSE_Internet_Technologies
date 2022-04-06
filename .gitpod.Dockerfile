FROM gitpod/workspace-full

COPY init.sh /tmp/setup-init.sh
RUN /tmp/setup-init.sh