# File Manager

**A unified interface for saving and loading files across various storage types.**

In modern applications, the need to read from and write to different storage
locations—such as local disk, cloud storage (e.g., AWS S3), or even mock locations for
testing—can quickly become complex and error-prone. Each storage type often comes with
its own APIs, libraries, and specific configurations, making it challenging to manage and
switch between them seamlessly. This package addresses these challenges by providing a
unified ``save()`` and ``load()`` interface that abstracts away the complexities of
interacting with different storage types. By simplifying this process, it allows
developers to easily swap storage backends without modifying their codebase, making it
ideal for environments that require flexible storage management, such as development,
testing, and production.

## Caution

While this package provides convenience in some use cases, it does come with some
trade-offs:

- **Limited Access to Specific Features:** By abstracting the underlying storage APIs,
the package may not expose all the specialized features or fine-tuned controls available
in specific storage types. If your application requires advanced, storage-specific
functionalities (e.g., S3-specific access control settings, versioning, or multipart
uploads), this package might not meet those needs without additional customization.

- **Potential Performance Overhead:** The abstraction layer introduces a small
performance overhead due to the generalized handling of different storage types. For
applications with high-performance requirements or large-scale data operations, this
might become a consideration.

- **Reduced Flexibility:** While the package aims to simplify storage interactions, it
also reduces flexibility by imposing a standardized interface. This can limit the ability
to fully exploit the unique capabilities of each storage type or to handle edge cases
specific to certain storage solutions.

- **Increased Complexity for Simple Use Cases:** For applications that only require
interaction with a single storage type (e.g., local filesystem only), using this package
might introduce unnecessary complexity. In such cases, directly using the relevant
storage API could be simpler and more straightforward.

## Example Usage

```python
from file_manager import FileManager

# some data to be saved and loaded as part of our project
data = {
    "name": "John Doe",
    "age": 30,
    "email": "johndoe@email.com"
}

# create a file manager instance
file_manager = FileManager(location_type="local", default_directory="data")

# use file manager to easily save and load file
file_manager.save(data, "data.json")
file_manager.load("data.json")
```