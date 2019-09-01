# Use an official Python runtime as a parent image
FROM python:2

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory to /mde
WORKDIR /mde

# Copy the current directory contents into the container at /app
COPY . /mde

RUN apt-get update \
    && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
    #
    # Verify git, process tools, lsb-release (common in install instructions for CLIs) installed
    && apt-get -y install git iproute2 procps lsb-release \
    #
    # Install PyQt4, as that's our GUI library
    && apt-get -y install python-qt4 python-qt4-doc \
    #
    # Install the enchant C library, for spell checking
    && apt-get -y install enchant \
    #
    # Update Python environment based on requirements.txt
    && pip --disable-pip-version-check --no-cache-dir install -r requirements.txt

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=

# Run app.py when the container launches
CMD ["python", "Main.py"]
