FROM osrf/ros:jazzy-desktop-full

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install common development tools and dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-argcomplete \
    git \
    vim \
    tmux \
    wget \
    curl \
    lsb-release \
    gnupg2 \
    bash-completion \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Install ROS2 Jazzy specific packages that might be useful for humanoid robotics
RUN apt-get update && apt-get install -y \
    ros-jazzy-xacro \
    ros-jazzy-joint-state-publisher-gui \
    ros-jazzy-robot-state-publisher \
    ros-jazzy-rviz2 \
    ros-jazzy-ros2-control \
    ros-jazzy-ros2-controllers \
    ros-jazzy-rmw-cyclonedds-cpp \
    && rm -rf /var/lib/apt/lists/*

# Setup non-root user
ARG USERNAME=devuser
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Delete existing user/group with UID/GID 1000 if they exist (common in Ubuntu 24.04 images)
RUN if getent passwd $USER_UID; then userdel -r $(getent passwd $USER_UID | cut -d: -f1); fi \
    && if getent group $USER_GID; then groupdel $(getent group $USER_GID | cut -d: -f1); fi \
    && groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Setup ROS2 environment for the user
RUN echo "source /opt/ros/jazzy/setup.bash" >> /home/$USERNAME/.bashrc \
    && echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> /home/$USERNAME/.bashrc

# Workspace setup
WORKDIR /workspace/ros2_ws

# Initialize rosdep
RUN rosdep update

# Set user
USER $USERNAME

# Default command
CMD ["bash"]
