# OpenBroadcaster Containers

This repository provides a containerized setup for running OpenBroadcaster and its supporting components, using Docker and Docker Compose. It is meant for development purposes, and not to be used in a production environment.

Tested and working with 5.3-develop branches as of 2024-12-22.
 - [https://github.com/openbroadcaster/observer](https://github.com/openbroadcaster/observer)
 - [https://github.com/openbroadcaster/obplayer](https://github.com/openbroadcaster/obplayer)

---

## **Contents**

- **Files**:
  - `docker-compose.yml`: Main Docker Compose configuration file to orchestrate all services.
  - `.env`: A file containing most of the configurations & build time arguments for openbroadcaster.

- **Directories**:
  - `icecast`: Configuration and container setup for the Icecast streaming server.
  - `mysql`: MySQL database setup and configuration.
  - `obplayer`: Configuration for the OBPlayer service.
  - `observer`: Configuration for the Observer service.

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

### 3. Default URLs and credentials

- **Observer Web Interface**:
   - Access the Observer service at [http://localhost:8080](http://localhost:8080).
   - Default username and password defined in .env.
   - Default username: admin
   - Default password: password
  
- **Obplayer Web Interface**:
   - Access the Obplayer web interface at [http://localhost:23233](http://localhost:23233).
   - Access the Live assist dashboard at [http://localhost:23456](http://localhost:23456).
   - Default username: admin
   - Default password: admin

- **Icecast Streaming Server**:
   - Access the Icecast server at [http://localhost:8000](http://localhost:8000).
   - Preview the stream at [http://localhost:8000/stream](http://localhost:8000/stream).
   - Default username and password defined in icecast.xml.
   - Default username: admin
   - Default password: hackme
  
---

### 4. First run

- **Upload Media to OBserver Web Interface**:
  - Login to Observer service at [http://localhost:8080](http://localhost:8080).
    - Default username and password defined in .env.
    - Default username: admin
    - Default password: password
    - Media > Upload media
    - Upload some MP3 files, and fill out the metadata.  Hit save.
  
- **Create playlist**:
  - From the Observer service at `http://localhost:8080`.
     - Playlists > New Playlist
    - Fill out the playlist data, and drag media items in.

- **Provision the Player**:
  - From the Observer service at `http://localhost:8080`.
    - Admin > Player Manager > New
    - Name = Obplayer
    - IP Address - leave blank
    - Password = 'password'
    - Media Types: Check all.
    - Timezone: (GMT-07:00) Pacific Time (Yukon)
    - Default Playlist: Your playlist you just created.
  
- **Enable and verify sync**:
  - From the Obplayer web interface at `http://localhost:23233`.
    - On the `Admin` tab
    - Import Settings > Choose File `/obplayer/obsettings.txt` > Import
    - Delete data.db and Restart `Restart`
    - Player should sync with server and icecast.
  - View the Live assist page `http://localhost:23456`
  - Preview the stream at `http://localhost:8000/stream`
- **Setup Complete**:

- **If needed - Manually Configure Sync**:
    - On the `Sync/Media` tab
    - Enable Scheduler/Sync [x]
    - Device ID = 1
    - Device Password = 'password'
    - Sync URL = `http://192.168.100.5/remote.php`.
    - Hit Save
    - Hit `Restart`
    - On the `Status` tab, check the [x] sync box, and make sure the server is connected.
    - The Audio Stream should show your media playing.
    - You can also enable the LiveAssist Dashboard from `Live Assist` > [x] Enable Live Assist
    - View the Live assist page `http://localhost:23456`

- **If needed - Manually Configure Icecast Stream**:
  - From the Obplayer web interface at `http://localhost:23233`.
    - On the `Streaming` tab
    - Enable Streaming [x]
    - Enable Icecast Streaming [x]
    - Icecast (One) Output Mode = Audio Only
    - Icecast (One) Output Bitrate = 320 kbps
    - Icecast (One) IP = 192.168.100.2
    - Icecast (One) Port = 8000
    - Icecast (One) Mountpoint = stream
    - Icecast (One) Username = source
    - Icecast (One) password = hackme
  - Preview the stream at `http://localhost:8000/stream`
  

## **Environment Variables**

Customize the services using the following environment variables stored in `.env` (examples can be found in `docker-compose.yml`):

- **MySQL**:
  - `MYSQL_ROOT_PASSWORD`: Root password for MySQL.
  - `MYSQL_DATABASE`: Name of the default database.
  - `MYSQL_USER`: Username for the database.
  - `MYSQL_PASSWORD`: Password for the database user.

- **Observer**:
  - `OBCONF_URL`: Base URL for the Observer service.
  - `OBCONF_EMAIL`: Admin email address.
  - `OBCONF_PASS`: Admin password.

---