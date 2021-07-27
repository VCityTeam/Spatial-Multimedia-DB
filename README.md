# Description of the Spatial Multimedia DB application

## Introduction

The goal of the Spatial Multimedia DB is to handle, and serve through 
[web services](https://en.wikipedia.org/wiki/Web_service), various types
of city related data in the context of 
[UD-SV (Urban Data Services and Vizualisation)](https://github.com/VCityTeam/UD-SV).

The API currently offers [web service](https://en.wikipedia.org/wiki/Web_service) 
access to few following types of resources :

- Documents (file and metadata)
- Guided tours (sequences of documents with additional texts)
- Links between documents and other (city) objects
- User accounts and rights

The service provided by the Spatial Multimedia DB is typically used by the
[UD-Viz web client/front-end](https://github.com/VCityTeam/UD-Viz/).

## Installation

In order to install and run the application (UNIX or Windows), refer to the installation
notes in [doc/Install.md]](doc/Install.md).

## Further information

### Architecture quick notes

This application provides all the expected
[CRUD operations](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) on the backend side.
Spatial Multimedia DB is developed in python and is based on an
[**MVC** (Model, View, Controller) architecture](doc/Design_Notes.md#MVC-architecture).
Persistance of objects to the DataBase is obtained through the usage of the [sqlalchemy library](https://www.sqlalchemy.org) together with an [**ORM**](https://en.wikipedia.org/wiki/Object-relational_mapping).
In order to wrap the (CRUD) service within an HTTP protocol (to deal with the requests and send responses to the client), the API uses the [flask library](http://flask.pocoo.org/docs/1.0/).

### How to use the API

The [API documentation](doc/API-Documentation.md) describes, among other
implementation details, the routes to be used to communicate with the server.

### Developer's notes

- **Decorator**
We use several times decorators in the application ,
In sake of code simplicity and readability, the code uses [(python) decorators](https://en.wikipedia.org/wiki/Python_syntax_and_semantics#Decorators). Because, at first, the understanding [decorators](https://en.wikipedia.org/wiki/Python_syntax_and_semantics#Decorators)
might not feel straightforward, you refer to this [decorators tutorial](doc/Decorators.md).

- **Diagram**
The diagram were mostly made with [Visual Paradigm](https://visual-paradigm.com/).
For further information on how you can modify them [refer to this Class diagram](doc/Class-diagrams.md).

