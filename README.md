# Py\_sched

A tool for automated generation (and submission) of jobscripts for standard schedulers and systems

## Motivation

Correct and reproducible computation is vital to produce trustworthy computation for science.
In HPC generating accurate submission scripts is particularly important, incorrect scripts might fail once they finally get through the queue, or worse hang in some unpredictable way using your time but not delivering results.
Py\_sched is a tool which aims to make (y)our life easier by providing an effient means of generating submission scripts for different schedulers and systems from common input files.

## Features

Currently under development:

* Supported schedulers
  1. PBS PRO
  2. Slrum

* Supported platforms
  1. Intel
  2. Gnu
  3. Cray

* Content
  1. Parallelism: Nodes, processes, processes per node, threads
  2. Module scripts
  3. Prelimary scripts
  4. Parallel execution
  5. Postscripts

## Usage


