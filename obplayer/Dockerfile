# Use the official Ubuntu 24.04 base image
FROM ubuntu:24.04

# Set non-interactive mode for apt
ENV DEBIAN_FRONTEND=noninteractive

# Pre-accept EULA for Microsoft fonts
RUN echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections

# Install dependencies and required tools
RUN apt update && \
    apt -y upgrade && \
    apt -y install \
        ntp python3 python3-pycurl python3-openssl python3-apsw python3-magic python3-dateutil \
        python3-requests python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-gdkpixbuf-2.0 \
        gir1.2-pango-1.0 python3-gst-1.0 gir1.2-gstreamer-1.0 gir1.2-gst-plugins-base-1.0 \
        gir1.2-gst-rtsp-server-1.0 gstreamer1.0-tools gstreamer1.0-libav gstreamer1.0-alsa \
        gstreamer1.0-pulseaudio gstreamer1.0-pipewire gstreamer1.0-plugins-base \
        gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly ffmpeg \
        ubuntu-restricted-addons ubuntu-restricted-extras gstreamer1.0-vaapi mesa-vdpau-drivers \
        espeak mbrola mbrola-en1 mbrola-us1 mbrola-us2 mbrola-us3 mbrola-fr1 mbrola-fr4 \
        python3-serial python3-pip git python3-boto3 python3-pulsectl python3-inotify \
        libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gtk-doc-tools meson && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Install gst-interpipe
RUN git clone https://github.com/RidgeRun/gst-interpipe.git /root/gst-interpipe && \
    cd /root/gst-interpipe && \
    mkdir build && \
    meson build --prefix=/usr && \
    ninja -C build && \
    ninja -C build install || echo "gtkdoc-tools error ignored"

# Clone and set up OpenBroadcaster Player
RUN git clone https://github.com/openbroadcaster/obplayer/ /usr/local/lib/obplayer && \
    cd /usr/local/lib/obplayer && \
    git checkout 5.3-staging

# Install CURL for network debugging
RUN apt-get update && apt-get install -y \
	curl iputils-ping

# Modify the regex in data.py to explicitly allow ob-server in the url_regex definition
RUN sed -i '/url_regex = re.compile/,/re.IGNORECASE/s/localhost|/localhost|ob-server|/' usr/local/lib/obplayer/obplayer/data.py

# Allow passwords to be exported
RUN sed -i 's/obplayer.Config.list_settings(hidepasswords=True).items()/obplayer.Config.list_settings(hidepasswords=False).items()/' usr/local/lib/obplayer/obplayer/httpadmin/httpadmin.py

# BUGFIX
RUN find . -type f -name "*.py" -exec sed -i 's/self.pipeline = Gst.Pipeline(name)/self.pipeline = Gst.Pipeline.new(name)/g' {} +

# Set working directory and provide executable entry
WORKDIR /usr/local/lib/obplayer

# Mount settings file
COPY obsettings.txt /app/obsettings.txt

# Startup script to import settings
COPY import_and_reset.py /usr/local/lib/obplayer/import_and_reset.py
RUN chmod +x /usr/local/lib/obplayer/import_and_reset.py

# Run import settings script
CMD ["python3", "/usr/local/lib/obplayer/import_and_reset.py"]

# Entry point for container
ENTRYPOINT /bin/bash ./obplayer_loop -H -d

EXPOSE 80
EXPOSE 443
EXPOSE 465
EXPOSE 25
EXPOSE 23456