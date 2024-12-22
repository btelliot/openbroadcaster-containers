# OpenBroadcaster Containers

This repository provides a containerized setup for running OpenBroadcaster and its supporting components, using Docker and Docker Compose. It is meant for development purposes, and not to be used in a production environment.

---

## **Contents**

- **Directories**:
  - `icecast`: Configuration and container setup for the Icecast streaming server.
  - `mysql`: MySQL database setup and configuration.
  - `obplayer`: Configuration for the OBPlayer service.
  - `observer`: Configuration for the Observer service.

- **Files**:
  - `docker-compose.yml`: Main Docker Compose configuration file to orchestrate all services.

---

## **Requirements**

- **Docker**: Ensure Docker is installed on your system. [Install Docker](https://docs.docker.com/get-docker/)

---

## **Getting Started**

### 1. Clone the Repository

```bash
git clone <repository-url>
cd openbroadcaster-containers
```

### 2. Build and Start the Containers

Use Docker Compose to build and run the containers:

```bash
docker-compose up --build
```

### 3. Access the Services

- **Observer Web Interface**:
  Access the Observer service at `http://localhost:8080` (or the IP/hostname of your Docker host).
  Default username and password defined in .env.
  Default username: admin
  Default password: password
  
- **Obplayer Web Interface**:
  Access the Obplayer web interface at `http://localhost:23233`.
  Default username: admin
  Default password: admin

- **Icecast Streaming Server**:
  Access the Icecast server at `http://localhost:8000`.
  Default username and password defined in icecast.xml.
  Default username: admin
  Default password: admin
  
- **MySQL Database**:
  Connect to the MySQL database using your preferred client. The configuration details are in the `mysql` directory or environment variables defined in `docker-compose.yml`.

---

### 4. First run

- **Upload Media**:
  Login to Observer service at `http://localhost:8080`.
    Media > Upload media
    Upload some MP3 files, and fill out the metadata.  Hit save.
  
- **Create playlist**:
  From the Observer service at `http://localhost:8080`.
    Playlists > New Playlist
	Fill out the playlist data, and drag media items in.


- **Provision the Player**:
  From the Observer service at `http://localhost:8080`.
    Admin > Player Manager > New
    Name = Obplayer
    IP Address - leave blank
    Password = 'password'
    Media Types: Check all.
    Timezone: (GMT-07:00) Pacific Time (Yukon)
    Default Playlist: Your playlist you just created.
  
  

## **Environment Variables**

Customize the services using the following environment variables (examples can be found in `docker-compose.yml`):

- **MySQL**:
  - `MYSQL_ROOT_PASSWORD`: Root password for MySQL.
  - `MYSQL_DATABASE`: Name of the default database.
  - `MYSQL_USER`: Username for the database.
  - `MYSQL_PASSWORD`: Password for the database user.

- **Observer**:
  - `OBCONF_URL`: Base URL for the Observer service.
  - `OBCONF_EMAIL`: Admin email address.
  - `OBCONF_PASS`: Admin password.

- **Icecast**:
  - `ICECAST_ADMIN_PASSWORD`: Admin password for Icecast.
  - `ICECAST_SOURCE_PASSWORD`: Source password for streaming.
  - `ICECAST_RELAY_PASSWORD`: Relay password for relaying streams.

---

## **Customizing Modules**

### Adding Modules

Use the following build arguments in the Dockerfile for Observer to add custom modules:
- `MODULE_NAMES`: Space-separated list of module names.
- `MODULE_REPOSITORIES`: Corresponding Git repository URLs for each module.

Example:
```bash
docker build --build-arg MODULE_NAMES="module1 module2" \
             --build-arg MODULE_REPOSITORIES="https://github.com/user/module1.git https://github.com/user/module2.git" \
             -t observer-custom .
```