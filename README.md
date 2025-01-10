# uv monospace example (ml system)

## Introduction

This repository contains an example monorepo that utilizes `uv` workspaces to
facilitate code sharing and project wheel building. It models a python codebase
for a machine learning inference system where a collection of distinct projects
(or equivalently, apps / endpoints) need to make selective use of a number of
private libraries and common shared dependencies. Such a system typically has
the following characteristics

- Some private libraries are project mixins, rather than globally shared.
  These mixins can have conflicting requirements. For example, one
  project might require access to various databases, whereas other projects
  are more stateless.
- Some private libraries might need to be published to PyPi for use in
  codebases external to the monorepo, such as in support infrastructure.
  Ideally this code is contained in the monorepo, but in practice this does not
  always happen.
- Projects typically utilize common helper packages that are used for model
  training and building (generally, development) but not for runtime inference.
- Some packages represent common runtime dependencies for some number of
  projects. As a real example, a collection of projects might all represent
  stateless fine-tuned transformer models deployed to near identical runtimes.
  These dependency sets are encoded in dummy packages that are specified in the
  project workspace.


One approach to handle this situation is to define a root-level dummy package
that includes the projects as dependency extras or groups. This allows common
sets of dev dependencies to be pulled automatically when
```sh
uv sync --extra {project}
```
is run at the dummy project root. For such a system, a global workspace with a
single lockfile can be unwieldy, as conflicting dependency conflicts need to be
combinatorially enumerated in the root `pyproject.toml`.

Instead, each project is given its own workspace with members explicitly
listed. This trades.

## Repo Structure

- `packages/shared` contains a virtual workspace of common shared dependencies
  that are often required together. There could potentially be multiple such
  virtual workspaces in a monorepo.
- `packages/dal` is another virtual workspace represents a data access layer.
  This is presented as a virtual workspace rather than individual packages
  since uv does not handle nested workspaces.
- `packages/deps` contains dummy packages specifying dependencies only, without
  any substantial code of their own. Conceptually they exist only to inject
  dependency sets into other packages. This is more of a convenience when
  working with many isolated project workspaces that all require, e.g., a core
  set of base dev dependencies. Also included here are packages that target
  common "runtime" dependencies.
- `packages/uvmono-ml` and `packages/uvmono-ml2` are isolated projects or
  applications with their own workspaces, lockfiles and developer envs. Each
  `pyproject.toml` file is explicit with its workspace members.
  They represent two distinct ml projects, i.e., inference tasks. These two
  packages would typically be deployed to distinct target runtimes, such as two
  different inference endpoints likely running with their own dedicated compute.
  Despite having isolated workspaces and lockfiles, they make use of similar
  private libs.


## Project development envs

To get a developer venv for the project `uvmono-ml` in the following
run in the monorepo root
```bash
uv sync --project packages/uvmono-ml
source packages/uvmono-ml/.venv/bin/activate
```

## Project wheel building

The `pyproject.toml` files for the `uvmono-ml` and `uvmono-ml2` projects
are very explicit about their workspace members. A collection of private wheels
for the project that can be either pushed to a container image and can be
built via

```bash
uv build --project packages/uvmono-ml --all-packages --wheel
```

## Todos

- [ ] Is there an easy way to build packages listed for some optional
  dependency as well, e.g., for when we need to including training and evaluation
  dependencies in some container? Ideally an invocation such as
  ```uv build --extra train --all-packages```.
