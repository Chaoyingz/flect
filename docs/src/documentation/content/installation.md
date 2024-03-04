# Installation Guide

This guide will help you install the necessary dependencies and assist you in setting up your application.

## Requirements

- Python 3.9 or higher

## Basic Installation

If you prefer to start a project from scratch, you can directly install the flect.

1. **Install flect**

   To install the flect, run the following command in your terminal:

   ```console
   pip install flect
   ```

## Installation Using Project Template (Recommended)

For those who prefer to use a project template to kickstart their application, follow these steps:

### Additional Requirements

- Rye (https://rye-up.com/) for dependency management
- Cookiecutter (https://cookiecutter.readthedocs.io/en/stable/) for project scaffolding

### Steps

1. **Create Project Structure**

   Use Cookiecutter to create the project structure by running:

   ```console
   cookiecutter https://github.com/Chaoyingz/cookiecutter-flect
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
   make dev
   ```

5. **Visit Your Application**

   Open your browser and visit http://127.0.0.1:8000 you will see the following page.

   ![welcome-to-flect](https://github.com/Chaoyingz/flect/assets/32626585/12c0f31b-8030-41b6-8c4b-3efb11e419ca)

By following these steps, you can either set up your project from scratch or use a pre-defined template to get started quickly.
