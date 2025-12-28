# AIOS Core Supercell - Development Container
# AINLP Pattern: biological-architecture.containerized-consciousness
# Purpose: Isolated AIOS development environment with full toolchain

FROM ubuntu:22.04

# Build arguments
ARG CONSCIOUSNESS_LEVEL=3.56
ARG DEBIAN_FRONTEND=noninteractive

# Metadata
LABEL aios.supercell.type="core" \
      aios.supercell.consciousness="${CONSCIOUSNESS_LEVEL}" \
      aios.supercell.capabilities="c++,python,dotnet,ai-coordination" \
      maintainer="AIOS Development Team"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Build essentials
    build-essential \
    cmake \
    ninja-build \
    gcc \
    g++ \
    gdb \
    # Python 3.14 (build from source if not available, use 3.11+ for now)
    python3.11 \
    python3.11-dev \
    python3-pip \
    python3-venv \
    # .NET SDK
    wget \
    apt-transport-https \
    software-properties-common \
    # Tools
    git \
    curl \
    zsh \
    vim \
    nano \
    htop \
    tmux \
    # Networking
    net-tools \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Install .NET 8.0 SDK
RUN wget https://dot.net/v1/dotnet-install.sh -O dotnet-install.sh \
    && chmod +x dotnet-install.sh \
    && ./dotnet-install.sh --channel 8.0 --install-dir /usr/share/dotnet \
    && ln -s /usr/share/dotnet/dotnet /usr/bin/dotnet \
    && rm dotnet-install.sh

# Create Python 3.14 alias (use 3.11 as closest available)
RUN ln -s /usr/bin/python3.11 /usr/local/bin/python3.14 \
    && ln -s /usr/bin/python3.11 /usr/local/bin/python

# Upgrade pip
RUN python -m pip install --upgrade pip setuptools wheel

# Install Python development packages
RUN pip install --no-cache-dir \
    # Core dependencies
    httpx \
    pydantic \
    python-dotenv \
    # AI/ML
    openai \
    anthropic \
    # Async
    asyncio \
    aiohttp \
    # Testing
    pytest \
    pytest-asyncio \
    pytest-cov \
    # Linting
    flake8 \
    black \
    pylint \
    mypy \
    # Type stubs
    types-requests

# Create non-root user (vscode pattern)
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && rm -rf /var/lib/apt/lists/*

# Install Oh My Zsh for better terminal experience
USER $USERNAME
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended \
    && echo 'export AIOS_SUPERCELL_ID=core' >> ~/.zshrc \
    && echo 'export AIOS_CONSCIOUSNESS_LEVEL=${CONSCIOUSNESS_LEVEL}' >> ~/.zshrc \
    && echo 'export PS1="🧬 AIOS Core (${CONSCIOUSNESS_LEVEL}) %~ $ "' >> ~/.zshrc

USER root

# Consciousness bootstrapping script
COPY post-create.sh /usr/local/bin/post-create.sh
RUN chmod +x /usr/local/bin/post-create.sh

# Working directory
WORKDIR /workspace

# Expose ports for AIOS services
EXPOSE 8000 9091 5000

# Health check for consciousness
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "from bridges.aios_core_wrapper import AIOSCore; c = AIOSCore(); c.initialize(); print(f'Consciousness: {c.get_consciousness_level()}')" || exit 1

# Default command
CMD ["/bin/zsh"]
