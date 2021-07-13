## Clone the repository (holding this directory)
You need to clone this repository with one of the following commands:
 - as a user: `git clone https://github.com/MEPP-team/UD-Serv.git`
 - as a developer, that is if you have an ssh key: `git clone git@github.com:MEPP-team/UD-Serv.git`

Then you need to connect to directory **API_Enhanced_City**: `cd UD-Serv/API_Enhanced_City`

*Note: In windows `/` is replaced by `\`*

## Install using docker
Modify the [.env](.env) file to match this configuration:

````
# database configuration
SPATIAL_MULTIMEDIA_ORDBMS=postgresql
SPATIAL_MULTIMEDIA_DB_USER=postgres
SPATIAL_MULTIMEDIA_DB_PASSWORD=password
SPATIAL_MULTIMEDIA_DB_HOST=postgres
SPATIAL_MULTIMEDIA_DB_PORT=5432
SPATIAL_MULTIMEDIA_DB_NAME=extendeddoc
````

> *Note: the .env that is commited should not be modified because it is used by travis for CI.*  
> Please make sure when you commit your files that you do not commit the `.env` file. If you see that `.env` appears in your changelog (in the `git status` command for example), you can prevent it from being commited using the command `git update-index --assume-unchanged .env`.

> Note: the default password for the administrator account (the one you must use to SignIn as `admin` within the web interface in order to declare users) is [not well documented](https://github.com/MEPP-team/UD-Serv/issues/89)... By default and in despair try using `password`.  

Then run the following commands:
````
sudo apt-get install docker
sudo apt-get install docker-compose
sudo systemctl start docker.service
sudo docker-compose build
sudo docker-compose up
````
In order to test that the server is indeed running, open `http://localhost:1525/` and assert that you get some response.
Note that the `1525` port number is the one configured (mapped for the `app` service) in the [docker-compose.yml](docker-compose.yml#L19) configuration file.

### Troubleshooting
 - **Problem with docker-compose**<br>
   If you get the following error when running `sudo docker-compose up` :
   ````
   ERROR: Version in "./docker-compose.yml" is unsupported. You might be seeing this
   error because you're using the wrong Compose file version. Either specify a version
   of "2" (or "2.0") and place your service definitions under the `services` key, or
   omit the `version` key and place your service definitions at the root of the file
   to use version 1.
   For more on the Compose file format versions, see https://docs.docker.com/compose/compose-file/
   ````
   You may need to check your version of docker-compose and update it by downloading the last stable version [here](https://docs.docker.com/compose/install/).

- **Cannot start service postgres**<br>
  If you get the following error when running `sudo docker-compose up` :
  ````
  Creating extended_doc_db ...
  Creating extended_doc_db ... error
  ERROR: for extended_doc_db  
  Cannot start service postgres: driver failed programming external connectivity on endpoint
     extended_doc_db (XXXX): 
  Error starting userland proxy: 
    listen tcp 0.0.0.0:5432: 
    bind: address already in use
  ERROR: for postgres  
  ERROR: Encountered errors while bringing up the project.
  ````
  You need to stop your local postgresql with the command `sudo service postgresql stop`.
  <br>
  You can also tell postgres to not start when booting with the command `sudo update-rc.d postgresql disable`

 - **Could not connect to server: Connection refused**<br>
   While running docker compose, if the database was successfully created but you get the following error :
   ```
   extended_doc_api | /api
   extended_doc_api | Trying to connect to Database...
   extended_doc_api | Config :  postgresql://postgres:password@postgres:5432/extendedDoc
   extended_doc_api | Connection failed (psycopg2.OperationalError) could not connect to server: Connection refused
   extended_doc_api |      Is the server running on host "postgres" (172.22.0.2) and accepting
   extended_doc_api |      TCP/IP connections on port 5432?
   extended_doc_api | 
   extended_doc_api | (Background on this error at: http://sqlalche.me/e/e3q8)
   ```
   It may be because the `.env` file is not correctly configured. Please make sure that your `.env` file matches the content shown above. Then, delete the database using :
   ```
   sudo rm -r postgres-data
   ```
   And rebuild the containers :
   ```
   sudo docker-compose build
   sudo docker-compose up
   ```

## Manual install  

### Install Python and PostgreSQL
[Python 3.6](https://www.python.org/downloads/) or newer is recommended and PostgreSQL can be install following
[this](https://www.postgresql.org/docs/9.3/static/tutorial-install.html).

### Create a (python) virtual environment
Then, create a virtual env in which we put the python intereter and our dependencies (only on Python3.6 or newer):
```
python3 -m venv venv
```

On **linux**, if it fails try to run the command below first: `sudo apt-get install python3-venv`

Enter in the virtual environment,
- On **Unix**: `source venv/bin/activate`
- on **Windows**: `venv\Scripts\activate.bat`

To quit the virtual environment, just type:   `deactivate`

***Warning**: Unless explicitly, in the following you need to be in the **virtual environment**.*

### Install packages
Required packages for the application:
- [**psycopg2**](http://initd.org/psycopg/)
- [**Sqlalchemy**](https://www.sqlalchemy.org/)
- [**Flask**](http://flask.pocoo.org/)
- [**PyYAML**](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [**Colorama**](https://pypi.org/project/colorama/)

Install them using: `pip3 install -r requirements.txt` where
`requirements.txt` contains the preceding packages.

### Create a postgres DataBase
You need to create a postgres database for instance on linux with
```
(root)$ sudo su postgres
(postgres)$ createuser citydb_user
(postgres)$ createdb -O citydb_user extendedDoc
(postgres)$ exit
```

*Note: You can also use [pgAdmin](https://www.pgadmin.org), especially on Windows.
It is a software like [PhpMyAdmin](https://www.phpmyadmin.net/) but for PostgreSQL database.
By default, it is installed with PostgreSQL: `Program Files (x86)\PostgreSQL\X.X\pgAdminX\bin\pgAdminX.exe`*

Then modify the [**.env**](.env) to reflect your configuration.
If you have created a new database as below, no change is needed but verify anyway everything are correct

```
SPATIAL_MULTIMEDIA_ORDBMS: postgresql
SPATIAL_MULTIMEDIA_DB_USER: citydb_user
SPATIAL_MULTIMEDIA_DB_PASSWORD: password
SPATIAL_MULTIMEDIA_DB_HOST: localhost
SPATIAL_MULTIMEDIA_DB_PORT: 5432
SPATIAL_MULTIMEDIA_DB_NAME: extendedDoc
```
The port number is (usually) configured in `/etc/postgresql/X.X/main/postgresql.conf` on Linux
and in `Program Files (x86)\PostgreSQL\X.X\data\postgresql.conf` on Windows

*Note: the exact location can change depending on your own configuration.*

## Execution

### Tests

To verify everything works fine, you can execute the tests files, located in the folder
[**test**](test)

By default, python will not find the local packages (such as **test** or **api**).
You thus need to add the location of **API_Enhanced_City** to the environment variable **PYTHONPATH** :
 - On **Linux**: `export PYTHONPATH="."`
 - On **Windows**: `set PYTHONPATH=.`
where the `.` (current directory) corresponds to the location of **API_Enhanced_City** and can be replaced
by any path to this directory.

Then you can run any test file located in the **test** directory, for instance:
```
python3 test/test_document.py
python3 test/test_guided_tour.py
```

*Note: if the tests don't run, verify that you have at least Python 3.6"

*Note: It is a good practice to launch the tests before running the server,
because it ensures everything works fine and is a way to have some data in the
database and facilitate the tests with the front-end.*

### Localhost execution

If you want the server to run you can then type: `python3 api/web_api.py`

### Production execution

#### Context

According to the [flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/deploy/)
it is a good practice to use a [production WSGI server](https://www.fullstackpython.com/wsgi-servers.html)

#### Configure and run uWSGI

Note that this part is only valid on the server `rict.lirirs.cnrs`, because of its environment.
A more detailed set up can be find on its server and its documentation.

 * Edit and adpat `Deployment/conf/API_Extended_Document.uwsgi.yml` to obtain something similar to

   ```
   uwsgi:
     virtualenv: /home/citydb_user/Demos/DocumentDemo/venv          <--- Adapt this
     master: true
     uid: citydb_user
     gid: citydb_user
     socket: /tmp/Api_Extended_Document-server.sock
     chmod-socket: 666
     module: api.web_api:app
     processes: 1
     enable-threads: true
     protocol: uwsgi
     need-app: true
     catch-exceptions: true
     log-maxsize: 10000000
     logto2: /home/citydb_user/Demos/DocumentDemo/uWSGI-server.log  <--- Adapt this
   ```

 * From the directory which contains the `Deployment` directory, launch the uWSGI server 
   ```
   (venv) $ uwsgi --yml Deployment/API_Extended_Document.uwsgi.yml --http-socket :9090
   ```

#### Save the documents located in the Database

To be sure to save your files, you can save tables into csv files:
```
psql extendedDoc -c “COPY extended_document TO ‘/tmp/extended_document-Id.csv’ DELIMITER ‘,’ CSV HEADER;”
psql extendedDoc -c “COPY visualisation TO ‘/tmp/extended_document-visualisation.csv’ DELIMITER ‘,’ CSV HEADER;” (edited)
psql extendedDoc -c “COPY metadata TO ‘/tmp/extended_document-metadata.csv’ DELIMITER ‘,’ CSV HEADER;”
```
