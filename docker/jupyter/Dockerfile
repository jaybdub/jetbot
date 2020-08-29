ARG BASE_IMAGE=jetbot-base:jp44
FROM ${BASE_IMAGE}

ARG JUPYTER_PASSWORD=jetbot
ENV JUPYTER_WORKDIR=/workspace
WORKDIR /workspace

# ====================
# SET JUPYTER PASSWORD
# ====================
ENV JUPYTER_CONFIG_DIR=/.jupyter
ENV JUPYTER_PASSWORD=${JUPYTER_PASSWORD}
RUN jupyter lab --generate-config -y
RUN python3 -c "from notebook.auth.security import set_password; set_password('${JUPYTER_PASSWORD}', '/.jupyter/jupyter_notebook_config.json')"    

ENV SHELL /bin/bash

RUN mkdir -p /.local
RUN chown -R 1000 \
	/usr/local/share/jupyter/lab/settings \
	/.local \
	${JUPYTER_CONFIG_DIR}

#RUN useradd -u 1000 -m jetbot
RUN useradd -m -u 1000 -G root jetbot
RUN usermod -d /workspace jetbot
USER jetbot

CMD cd $JUPYTER_WORKDIR && jupyter lab --ip 0.0.0.0 --port 8888 
