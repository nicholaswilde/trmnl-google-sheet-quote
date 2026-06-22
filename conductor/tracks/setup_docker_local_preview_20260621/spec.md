# Specification: Docker Local Preview Setup

## Overview
Enable seamless local testing of the TRMNL plugin using a Docker-based environment wrapper.

## Requirements
- Add a script named `preview:docker` to `package.json` that automates running the `usetrmnl/trmnlp` Docker container with volume mapping.
- Update `tech-stack.md` to document Docker in the development toolchain.
- Document the local testing workflow (running, opening `http://localhost:4567`) in `README.md`.

## Acceptance Criteria
- `package.json` has the `preview:docker` script.
- `README.md` contains clear copy-pasteable instructions for running via Docker.
