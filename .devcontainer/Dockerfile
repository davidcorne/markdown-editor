FROM debian:latest

# Set the working directory to /mde
WORKDIR /mde

# Copy the current directory contents into the container at /app
COPY . /mde
# Update apt sources
RUN echo 'deb http://ftp.utexas.edu/debian/ jessie main contrib' |tee -a /etc/apt/sources.list
RUN echo 'deb-src http://ftp.utexas.edu/debian/ jessie main contrib' |tee -a /etc/apt/sources.list

# Install Qt4
RUN apt-get update && \
    apt-get install -y \
	git \
	wget \
	curl \
    python-dev \
    python-pip \
    build-essential \
	python-qt4 \
	pyqt4-dev-tools \
    libqtwebkit4 \
    #
    # Install the enchant C library, for spell checking
    enchant \
    #
    # Update Python environment based on requirements.txt
    && pip --disable-pip-version-check --no-cache-dir install -r requirements.txt

# Clean packages
RUN apt-get clean

