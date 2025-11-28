#!/bin/bash
# Bootstrap script for Everest agent that runs SvF inside a Docker image.
# Usage (inside Everest plan):
#   command /usr/local/bin/runSvF-remote-agent.sh ${docker_image_tag}

set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <docker_image_tag> [extra args...]" >&2
  exit 1
fi

DOCKER_TAG="$1"
shift

# Base image repository; can be overridden via environment
SVF_IMAGE_REPO="${SVF_IMAGE_REPO:-ghcr.io/distcomp/svf}"
IMAGE="${SVF_IMAGE_REPO}:${DOCKER_TAG}"

echo "Using SvF image: ${IMAGE}"

if [[ "${DOCKER_TAG}" == cached-* ]]; then
  # Cached (pinned) images: pull only if missing
  if ! docker image inspect "${IMAGE}" >/dev/null 2>&1; then
    echo "Cached image ${IMAGE} not found locally, pulling from registry..."
    if ! docker pull "${IMAGE}"; then
      echo "ERROR: Failed to pull ${IMAGE}" >&2
      exit 1
    fi
  fi
else
  # Floating branch tags: always pull latest version
  echo "Pulling latest image for tag ${DOCKER_TAG}..."
  if ! docker pull "${IMAGE}"; then
    echo "ERROR: Failed to pull ${IMAGE}" >&2
    exit 1
  fi
fi

WORKDIR="$(pwd)"
echo "Working directory: ${WORKDIR}"

child_pid=""
forward_sigint() {
  if [ -n "${child_pid}" ] && kill -0 "${child_pid}" 2>/dev/null; then
    echo "Forwarding SIGINT to docker run (pid=${child_pid})..."
    kill -INT "${child_pid}" || true
    wait "${child_pid}" || true
  fi
  exit 130
}
trap forward_sigint INT

docker run --rm \
  -v "${WORKDIR}:${WORKDIR}" \
  -w "${WORKDIR}" \
  -e EVEREST_TASK_TOKEN \
  "${IMAGE}" \
  /usr/local/bin/runSvF-remote.sh "$@" &

child_pid=$!
wait "${child_pid}"


