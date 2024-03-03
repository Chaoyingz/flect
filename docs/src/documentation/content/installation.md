# Installation Guide

This guide will help you install the necessary dependencies and assist you in setting up your application.

## Requirements

- Python 3.9 or higher

## Basic Installation

If you prefer to start a project from scratch, you can directly install the tui framework.

1. **Install tui framework**

   To install the tui framework, run the following command in your terminal:

   ```console
   pip install tuiframework
   ```

## Installation Using Project Template

For those who prefer to use a project template to kickstart their application, follow these steps:

### Additional Requirements

- Rye (https://github.com/Chaoyingz/rye) for dependency management
- Cookiecutter (https://cookiecutter.readthedocs.io/en/stable/) for project scaffolding

### Steps

1. **Create Project Structure**

   Use Cookiecutter to create the project structure by running:

   ```console
   cookiecutter https://github.com/Chaoyingz/tui/tree/main/src/python-tui/src/cookiecutter-tui
   ```

2. **Navigate to Project Directory**

   Change into your project's directory:

   ```console
   cd {project_slug}
   ```

3. **Synchronize Dependencies**

   Use Rye to synchronize your project's dependencies:

   ```console
   rye sync
   ```

4. **Run Your Application**

   Start your application with Uvicorn:

   ```console
   uvicorn src.{project_slug}.main:app
   ```

By following these steps, you can either set up your project from scratch or use a pre-defined template to get started quickly.
