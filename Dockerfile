#Last package update 29 June 2024
FROM lscr.io/linuxserver/radarr:latest
LABEL Maintainer="bizalu"

# Prepare python environment
ENV PYTHONUNBUFFERED=1
RUN apk add --no-cache python3 py3-defusedxml
RUN apk -U upgrade --no-cache
RUN if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi

# Install custom post files
COPY services/ /etc/s6-overlay/s6-rc.d/
RUN find /etc/s6-overlay/s6-rc.d/ -name run -exec chmod u+x {} \;

# Install custom init script
COPY custom-script-init/ /custom-cont-init.d/
RUN chmod u+x /custom-cont-init.d/*

# Install custom post script
COPY custom-script/ /etc/cont-post.d/
RUN chmod u+x /etc/cont-post.d/*