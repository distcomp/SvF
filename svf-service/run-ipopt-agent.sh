#!/bin/bash
# Bootstrap script for Everest agent to run Ipopt jobs inside SvF+solvers image.
# Usage in Everest plan (conceptual):
#   command /usr/local/bin/run-ipopt.sh ${docker_image_tag} ${nlname} ${options}

set -euo pipefail

if [ $# -lt 3 ]; then
  echo "Usage: $0 <docker_image_tag> <nlname> <options_file> [extra args...]" >&2
  exit 1
fi

DOCKER_TAG="$1"
shift

NLNAME="$1"
OPTS_FILE="$2"
shift 2

SVF_IMAGE_REPO="${SVF_IMAGE_REPO:-ghcr.io/distcomp/svf}"
IMAGE="${SVF_IMAGE_REPO}:${DOCKER_TAG}"

echo "Using SvF+solvers image for Ipopt: ${IMAGE}"

if [[ "${DOCKER_TAG}" == cached-* ]]; then
  if ! docker image inspect "${IMAGE}" >/dev/null 2>&1; then
    echo "Cached image ${IMAGE} not found locally, pulling from registry..."
    docker pull "${IMAGE}"
  fi
else
  echo "Pulling latest image for tag ${DOCKER_TAG}..."
  docker pull "${IMAGE}"
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
  "${IMAGE}" \
  /usr/local/bin/run-ipopt.sh "${NLNAME}" "${OPTS_FILE}" "$@" &

child_pid=$!
wait "${child_pid}"


