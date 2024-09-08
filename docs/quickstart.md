# Quickstart

## Installation

TODO

## Basic Usage

TODO

## Configuration Driven Usage

One of the more powerful ways to make use of the ``file_manager`` package is to use
configuration driven file handling, which makes it easy to manage storage location
details for different environments (e.g. local, development, production) and to
switch between them with minimal effort. It might look something like this:

```yaml
# config.yaml
dev:
    location_type: "local"
    handler_kwargs:
prod:
    location_type: "s3"
    handler_kwargs:
        bucket_name: "my_bucket"
        path_prefix: "my_project"
```

```python
from file_manager import FileManager
import yaml
import os

# Load configuration from yaml file
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Determine file handler configuration based on environment
env = os.getenv("PYTHON_PROJECT_ENV", "dev")
location_type = config[env]["location_type"]
handler_config = config[env]["handler_kwargs"]

# Basic function intended to imitate a typical workflow
def main():
    file_manager = FileManager(
        default_directory="data",
        location_type=location_type,
        handler_kwargs=handler_config,
    )
    raw_data = file_manager.load("raw_data.csv")
    # do some processing here...
    file_manager.save("processed_data.csv", processed_data)
```


## Path Prefix for Shared Storage Locations

Location types intended for shared storage (e.g. Amazon S3, or Google Cloud Services)
will typically have a ``path_prefix`` parameter as part of their file handler's
instantiation method. This parameter is used to specify a common prefix for all files
stored in that location and is useful for maintaining consistency between local storage
and shared storage location types. For example, if you're working on a project locally,
called ``my_project`` let's say, then you will likely have a path for storing your data
that is relative to the root of the project called something like `data/`. This path may
also contain subdirectories, such as `data/raw_data/` or `data/outputs/` for storing data
that is specific to certain stages of the project's workflow. Importantly, due to the
self-contained nature of projects, this path is sufficient for storing data locally
without the need to prefix it with the project name (creating something like 
`my_project/data/`). However, when it comes to utilizing a shared storage location type
(e.g. Amazon S3), it's highly possible that all your storage paths are relative to some
root directory that is shared between multiple projects (a shared S3 bucket in Amazon
case). Because of this, we need a way to drill down one more level to create a project
specific path within the shared storage location. This is where the `path_prefix`
parameter comes in.
