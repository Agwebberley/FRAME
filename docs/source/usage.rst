Usage
=====

There are two primary purposes for this library:
1. To provide a faster way to build Django applications.
2. To provide a standard way to build Django applications.

Frame changes the way you interact with models as compared to the traditional Django ORM.
There should be significantly less code needed to bootstrap new models and forms while keeping direct access to code when needed.
Many similar solutions compromise on flexibility, especially when you leave the so-called "CRUD happy path."

.. toctree::
    :maxdepth: 2
    
    usage/models
    usage/views
    usage/admin
    usage/aws
