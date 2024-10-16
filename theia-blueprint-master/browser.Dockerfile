# Builder stage
FROM node:18-bullseye as build-stage

# install required tools to build the application
RUN apt-get update && apt-get install -y libxkbfile-dev libsecret-1-dev

WORKDIR /home/theia

# Copy repository files
COPY . .

# Remove unnecesarry files for the browser application
# Download plugins and build application production mode
# Use yarn autoclean to remove unnecessary files from package dependencies
RUN yarn --pure-lockfile && \
    yarn build:extensions && \
    yarn download:plugins && \
    yarn browser build && \
    yarn && \
    yarn autoclean --init && \
    echo *.ts >> .yarnclean && \
    echo *.ts.map >> .yarnclean && \
    echo *.spec.* >> .yarnclean && \
    yarn autoclean --force && \
    yarn cache clean && \
    rm -rf .git applications/electron theia-extensions/launcher theia-extensions/updater node_modules

# Production stage uses a small base image
FROM node:18-bullseye-slim as production-stage

# Create theia user and directories
# Application will be copied to /home/theia
# Default workspace is located at /home/project
RUN adduser --system --group theia
RUN chmod g+rw /home && \
    mkdir -p /home/project && \
    chown -R theia:theia /home/theia && \
    chown -R theia:theia /home/project;

# Install required tools for application: Temurin JDK, JDK, SSH, Bash, Maven
# Node is already available in base image
RUN apt-get update && apt-get install -y wget apt-transport-https && \
    wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public | tee /usr/share/keyrings/adoptium.asc && \
    echo "deb [signed-by=/usr/share/keyrings/adoptium.asc] https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | tee /etc/apt/sources.list.d/adoptium.list && \
    apt-get update && apt-get install -y git openssh-client openssh-server bash libsecret-1-0 temurin-17-jdk maven && \
    apt-get purge -y wget && \
    apt-get clean

ENV HOME /home/theia
WORKDIR /home/theia

# Copy application from builder-stage
COPY --from=build-stage --chown=theia:theia /home/theia /home/theia

EXPOSE 3000

# Specify default shell for Theia and the Built-In plugins directory
ENV SHELL=/bin/bash \
    THEIA_DEFAULT_PLUGINS=local-dir:/home/theia/plugins

# Use installed git instead of dugite
ENV USE_LOCAL_GIT true

# CUSTOM conda
ARG MINIFORGE_NAME=Miniforge3
ARG MINIFORGE_VERSION=24.7.1-2
ARG TARGETPLATFORM

ENV CONDA_DIR=/opt/conda
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH=${CONDA_DIR}/bin:${PATH}

# 1. Install just enough for conda to work
# 2. Keep $HOME clean (no .wget-hsts file), since HSTS isn't useful in this context
# 3. Install miniforge from GitHub releases
# 4. Apply some cleanup tips from https://jcrist.github.io/conda-docker-tips.html
#    Particularly, we remove pyc and a files. The default install has no js, we can skip that
# 5. Activate base by default when running as any *non-root* user as well
#    Good security practice requires running most workloads as non-root
#    This makes sure any non-root users created also have base activated
#    for their interactive shells.
# 6. Activate base by default when running as root as well
#    The root user is already created, so won't pick up changes to /etc/skel
RUN apt-get update > /dev/null && \
    apt-get install --no-install-recommends --yes \
        wget bzip2 ca-certificates \
        git \
        tini \
        > /dev/null && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    wget --no-hsts --quiet https://github.com/conda-forge/miniforge/releases/download/${MINIFORGE_VERSION}/${MINIFORGE_NAME}-${MINIFORGE_VERSION}-Linux-$(uname -m).sh -O /tmp/miniforge.sh && \
    /bin/bash /tmp/miniforge.sh -b -p ${CONDA_DIR} && \
    rm /tmp/miniforge.sh && \
    conda clean --tarballs --index-cache --packages --yes && \
    find ${CONDA_DIR} -follow -type f -name '*.a' -delete && \
    find ${CONDA_DIR} -follow -type f -name '*.pyc' -delete && \
    conda clean --force-pkgs-dirs --all --yes  && \
    echo ". ${CONDA_DIR}/etc/profile.d/conda.sh && conda activate base" >> /etc/skel/.bashrc && \
    echo ". ${CONDA_DIR}/etc/profile.d/conda.sh && conda activate base" >> ~/.bashrc
# CUSTOM END conda 

# Swtich to Theia user
USER theia
WORKDIR /home/theia/applications/browser

# Launch the backend application via node
ENTRYPOINT [ "node", "/home/theia/applications/browser/lib/backend/main.js" ]

# Arguments passed to the application
CMD [ "/home/project", "--hostname=0.0.0.0" ]
