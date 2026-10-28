# PR Summary: Add export pipeline

## Overview

Adds a background export pipeline that serializes reports to CSV.

## Changes

- adds `Exporter` with a queue-backed worker
- adds a `/export` endpoint accepting a report id
- registers the worker in the service wiring

**[TRIAGE]:** NEEDS_REVIEW
