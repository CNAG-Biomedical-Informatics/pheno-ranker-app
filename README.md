# Pheno-Ranker App

A standalone desktop application for phenotype ranking using the Pheno-Ranker tool, built with Python and CustomTkinter.

## Overview

**Pheno-Ranker App** is a desktop application that provides a user-friendly graphical interface for the Pheno-Ranker tool. Designed for researchers and clinicians in genetics and bioinformatics, it simplifies phenotype ranking by offering an intuitive interface to input data, configure options, and visualize results.

This application is built with Python and utilizes the [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) library for an enhanced GUI experience. It integrates the **Pheno::Ranker** Perl module from CPAN, ensuring robust and reliable phenotype analysis.

## Features

- **User-Friendly Interface**: Simplifies phenotype ranking with an intuitive GUI.
- **Multiple Modes**:
  - **Cohort Mode**: Analyze multiple reference phenotype files.
  - **Patient Mode**: Compare a target phenotype file against reference files.
- **Dynamic Input Handling**: Easily add multiple reference files.
- **Advanced Options**: Access and configure advanced settings for customized analyses.
- **Visualization**:
  - Generates heatmaps and displays them within the application.
  - Supports dynamic resizing and updating of visual outputs.
- **Error Handling**: Enhanced validation and error messages to guide users.
- **Integration with Pheno::Ranker**: Leverages the powerful Pheno::Ranker Perl module for analysis.

## Getting Started

### Prerequisites

- **Docker**: Ensure you have [Docker](https://www.docker.com/get-started) installed on your system.

### Docker Installation

A Dockerfile is provided to set up the application in a containerized environment.

#### Build the Docker Image

The Dockerfile uses `wget` to download the repository directly during the build process. To build the image, simply run:

```bash
wget https://raw.githubusercontent.com/mrueda/pheno-ranker-app/refs/heads/main/Dockerfile
docker build -t pheno-ranker-app .
```

#### Run the Docker Container

```bash
docker run -it --rm pheno-ranker-app
```
