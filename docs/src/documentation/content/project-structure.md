# flect project structure

This document provides an overview of the project structure for a flect application, with a focus on routing conventions.

## Routing Conventions

Understanding the routing conventions is crucial for navigating through a flect application. Here are the key components and their functions:

### Routing Files

- `layout.py`: This file defines the User Interface (UI) shared across all routes. It sets the common layout for different pages in the application.

- `page.py`: This file is responsible for the UI unique to a specific route. Each unique page in the application corresponds to a `page.py` file.

- `route.py`: This file defines the API endpoint for a specific route.

### Nested Routes

Nested routes allow for a hierarchical structure in the application's navigation:

- `folder`: Represents a route segment.

- `folder/folder`: Represents a nested route segment. It's a sub-route within a main route segment.

### Dynamic Routes

Dynamic routes allow for more flexible navigation paths:

- `dynamic__{folder}`: Represents a dynamic route segment. The route can change based on certain conditions or parameters.

### Route Groups

Route groups help organize related routes without affecting the actual routing:

- `group__{folder}`: Represents a group of related routes. This does not affect the routing but helps in organizing similar routes together.
