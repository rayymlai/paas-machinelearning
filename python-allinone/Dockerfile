# Program: Dockerfile
# Purpose: cpu (non-gpu) python container for machine learning, python 3
#          modified from multiple github projects, and add custom extension, e.g. password control, ssh access, flask
# Author:  Ray Lai
# Sources: https://github.com/uetchy/dockerfile-machinelearning/blob/master/Dockerfile
#          https://github.com/floydhub/dl-docker/blob/master/Dockerfile.cpu
# Features: (1) Python 3, (2) pre-loaded with popular machine learning lib, (3) web app via flask, port 5000
#           (4) jupyter notebook, port 8888, (5) SSH via port 22
# Updated: Aug 10, 2017
# License: MIT
#
FROM ubuntu:latest
MAINTAINER Ray Lai "rayymlai@gmail.com"

# For interactive packages
ENV TERM xterm

# Install base image, assume Python 2.7
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install -y sudo curl vim wget git cmake pkg-config unzip imagemagick libgtk2.0-dev
RUN apt-get clean
RUN apt-get autoremove 
RUN pip install --upgrade pip

# install SSH
RUN apt-get install -y openssh-server openssh-client
RUN mkdir /var/run/sshd
# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
RUN apt-get clean 
RUN apt-get autoremove

# Set up Python virtual env
RUN pip install virtualenv
RUN virtualenv venv
RUN . venv/bin/activate

# Install machine learning lib/framework
ENV CUDA_HOME /usr/local/cuda

# Install miniconda3 for Python 3.x
ENV PATH /opt/conda/bin:$PATH
ENV LB_LIBRARY_PATH /opt/conda/lib:$LB_LIBRARY_PATH
RUN curl -Ls https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -o /tmp/install-miniconda.sh && \
    /bin/bash /tmp/install-miniconda.sh -b -p /opt/conda && \
    conda update --all -y

# Upgrade pip
RUN curl -O https://bootstrap.pypa.io/get-pip.py && \
	python get-pip.py && \
	rm get-pip.py

# Basic dependencies
RUN conda install -y bzip2 glib readline mkl openblas numpy scipy hdf5 \
    pillow matplotlib cython pandas gensim protobuf \
    lmdb leveldb boost glog gflags
RUN pip install pydot_ng nnpack h5py scikit-learn scikit-image && \
    python -c 'import h5py;h5py.run_tests()'

# install system dependencies
RUN apt-get install -y bc build-essential cmake curl git nano unzip vim wget pkg-config python-dev 
RUN apt-get install -y g++ gfortran libffi-dev libfreetype6-dev libhdf5-dev libjpeg-dev liblcms2-dev libopenblas-dev
RUN apt-get install -y liblapack-dev libopenjpeg5 libpng12-dev libssl-dev libtiff5-dev libwebp-dev libzmq3-dev 
RUN apt-get install -y software-properties-common zlib1g-dev qt5-default libvtk6-dev zlib1g-dev libjpeg-dev libwebp-dev
RUN apt-get install -y libpng-dev libtiff5-dev libjasper-dev libopenexr-dev libgdal-dev libdc1394-22-dev libavcodec-dev
RUN apt-get install -y libavformat-dev libswscale-dev libtheora-dev libvorbis-dev libxvidcore-dev libx264-dev
RUN apt-get install -y yasm libopencore-amrnb-dev libopencore-amrwb-dev libv4l-dev libxine2-dev 
RUN apt-get install -y libtbb-dev libeigen3-dev python-dev python-tk python-numpy python3-dev python3-tk 
RUN apt-get install -y python3-numpy ant default-jdk doxygen
RUN apt-get clean
RUN apt-get autoremove
RUN rm -rf /var/lib/apt/lists/* && \
# Link BLAS library to use OpenBLAS using the alternatives mechanism (https://www.scipy.org/scipylib/building/linux.html#debian-ubuntu)
	update-alternatives --set libblas.so.3 /usr/lib/openblas-base/libblas.so.3

# Add SNI support to Python
RUN pip --no-cache-dir install pyopenssl ndg-httpsclient pyasn1

# Install useful Python packages using apt-get to avoid version incompatibilities with Tensorflow binary
# especially numpy, scipy, skimage and sklearn (see https://github.com/tensorflow/tensorflow/issues/2034)
RUN apt-get update
RUN apt-get install -y python-numpy python-scipy python-nose python-h5py python-skimage python-matplotlib python-pandas
RUN apt-get install -y python-sklearn python-sympy
RUN apt-get clean
RUN apt-get autoremove
RUN rm -rf /var/lib/apt/lists/* 

# Install other useful Python packages using pip
#RUN pip --no-cache-dir install --upgrade ipython 
#RUN pip --no-cache-dir install \
#		Cython \
#		ipykernel \
#		jupyter \
#		path.py \
#		Pillow \
#		pygments \
#		six \
#		sphinx \
#		wheel \
#		zmq \
#		&& \
#RUN python -m ipykernel.kernelspec

# OpenCV
RUN conda install -y -c menpo opencv3 && \
    python -c "import cv2;print(cv2.__version__)"

RUN ldconfig

# Install nltk
RUN pip install -q nltk

# Jupyter
RUN pip install -q jupyter jupyterlab && \
    jupyter --version

# Add jupyter default notebook password
RUN jupyter notebook --allow-root --generate-config
COPY jupyterPassword.txt /root/.jupyter/jupyter_notebook_config.py

COPY runner.sh /usr/src/app/runner.sh

WORKDIR /usr/src/app
VOLUME /usr/src/app

# TensorFlow
RUN git clone --depth 1 https://github.com/tensorflow/tensorflow.git /usr/src/tensorflow && \
    pip install tensorflow

# Install flask
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

# Entrypoint for Python container with Flask
# ENTRYPOINT ["python"]
# CMD ["app.py"]

# start jupyter notebook
#RUN jupyter notebook --no-browser --ip='*' --allow-root

# change working directory, /opt/src should be mapped to your shared data volume with git
WORKDIR /opt/src

EXPOSE 22
EXPOSE 5000
EXPOSE 8888
CMD ["/usr/sbin/sshd", "-D"]
