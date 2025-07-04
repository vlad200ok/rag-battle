ARG BASE_IMAGE=ubuntu:22.04
FROM $BASE_IMAGE AS builder
COPY --from=ghcr.io/astral-sh/uv:0.6.13 /uv /uvx /bin/

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

# Select python version
ARG PYTHON_VERSION=3.11

# UV_LINK_MODE changes how packages are installed from the global cache.
# Instead of creating hard links, the package files are copied to the virtual
# environment directory `site-packages`. This is necessary for future copying of
# the isolated `/app` directory from the `build` stage to the final Docker image.
ENV UV_LINK_MODE=copy

# UV_COMPILE_BYTECODE - enables compilation of Python files to bytecode after
# installation. https://docs.astral.sh/uv/configuration/environment/
ENV UV_COMPILE_BYTECODE=1

# PYTHONOPTIMIZE - removes `assert` instructions and code that depends on the
# value of the `__debug__` constant, when compiling Python files to bytecode.
# https://docs.python.org/3/using/cmdline.html#environment-variables
ENV PYTHONOPTIMIZE=1

# Configure the venv directory so it is consistent
ENV UV_PROJECT_ENVIRONMENT=/venv

# Configure the Python directory so it is consistent
ENV UV_PYTHON_INSTALL_DIR=/python

# PATH - adds the virtual environment directory `bin` to the beginning of the list
# of directories with executables. This allows Python utilities to be run from
# any directory in the container without specifying the full file path.
ENV PATH="/venv/bin:$PATH"

# Only use the managed Python version
ENV UV_PYTHON_PREFERENCE=only-managed

# This timeout (in seconds) is necessary when installing some dependencies via uv since
# it's likely to time out. Reference: https://github.com/astral-sh/uv/pull/1694
ENV UV_HTTP_TIMEOUT=3600
# Controls the number of threads used when installing and unzipping packages.
# We may need it to avoid ulimits change.
#ENV UV_CONCURRENT_INSTALLS=8

# Install python.
RUN uv python install $PYTHON_VERSION

# UV_PYTHON_DOWNLOADS disables automatic downloading of missing Python versions.
ENV UV_PYTHON_DOWNLOADS=never

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y \
    curl \
    ca-certificates \
    build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# install requirements
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source="uv.lock",target=uv.lock \
    --mount=type=bind,source="pyproject.toml",target=pyproject.toml \
    uv sync --frozen --no-dev

ARG USER=docker_user
# DEV_ENV is used to install development specific packages like pytest.
ARG DEV_ENV="0"

# Install dev dependencies if we are in development environment(root or it was
# requested directly)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source="uv.lock",target=uv.lock \
    --mount=type=bind,source="pyproject.toml",target=pyproject.toml \
    if [ "$USER" = "root" ] || [ "$DEV_ENV" != "0" ]; then \
        uv sync; \
    fi

# Install pip for convenience
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install pip

# Copy code
COPY rag_battle .
COPY main.py .

ARG BASE_IMAGE=ubuntu:22.04
FROM $BASE_IMAGE AS final
# Install the uv package manager. It is used to install nltk and tiktoken tokenizer
# on this stage, as they can't be installed on the build stage.
COPY --from=ghcr.io/astral-sh/uv:0.6.13 /uv /uvx /bin/

# PYTHONOPTIMIZE - tells the Python interpreter to use previously compiled files from
# the `__pycache__` directory with the suffix `opt-1` in the name.
ENV PYTHONOPTIMIZE=1
# PYTHONFAULTHANDLER - sets error handlers for additional signals.
ENV PYTHONFAULTHANDLER=1
# PYTHONUNBUFFERED - disables buffering for stdout and stderr streams to make sure
# all messages always reach console
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y \
    curl \
    ca-certificates \
    build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy python from the builder.
COPY --from=builder /python /python

# Copy venv from the builder.
COPY --from=builder /venv /venv

# PATH - adds the virtual environment directory `bin` to the beginning of the list
# of directories with executables. This allows Python utilities to be run from
# any directory in the container without specifying the full file path.
ENV PATH="/venv/bin:$PATH"

ARG USER=docker_user
ENV UV_PROJECT_ENVIRONMENT=/venv

# Update system
ARG CACHEBUST="0"
RUN if [ "$CACHEBUST" != "0" ]; then \
        echo $CACHEBUST && \
        apt-get update && \
        apt-get upgrade -y && \
        apt-get clean && \
        rm -rf /var/lib/apt/lists/*; \
    fi
RUN useradd --create-home --uid 1001 docker_user

# Copy the application from the builder.
COPY --from=builder /app /app

USER ${USER}
WORKDIR /app

CMD python main.py