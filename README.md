# Zero Trust Network Simulation

This project simulates a Zero Trust Network (ZTN) using Docker, Flask, iptables, and Fluentd. The setup includes network segmentation, strong authentication mechanisms, detailed access controls, and advanced monitoring tools.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [What it Does](#what-it-does)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before you begin, ensure you have the following installed:

- Docker
- Docker Compose
- Python 3.8 or later
- `pip` (Python package installer)

## Setup

1. **Clone the Repository:**

    ```sh
    git clone https://github.com/yourusername/zero-trust-network-simulation.git
    cd zero-trust-network-simulation
    ```

2. **Install Python Dependencies:**

    Create a file named requirements.txt and input the following:
   ```txt
    Flask==2.0.2
    Authlib==0.15.5
    PyJWT==2.3.0
    colorlog==6.6.0
   ```
   Then, navigate to each service directory and install the required packages: 

    ```sh
    cd oauth2_server
    pip install -r requirements.txt
    cd ../internal_service
    pip install -r requirements.txt
    cd ../dmz_service
    pip install -r requirements.txt
    cd ../external_service
    pip install -r requirements.txt
    ```

4. **Build and Start the Docker Containers:**

    ```sh
    docker-compose up -d --build
    ```

5. **Configure iptables for Policy Enforcement:**

    ```sh
    sudo bash setup_iptables.sh
    ```

## Usage

The project simulates a Zero Trust Network by creating isolated network segments and enforcing strict access controls. Each service runs in its own Docker container and communicates according to the Zero Trust principles.

- **OAuth2 Server:** Provides token-based authentication.
- **Internal Service:** A protected service that requires valid tokens.
- **DMZ Service:** Represents a service in the DMZ (Demilitarized Zone).
- **External Service:** Represents an external-facing service.
- **Fluentd:** Collects and logs network traffic.

### Accessing the Services

- **OAuth2 Server:** `http://localhost:5000/token`
- **Internal Service:** `http://localhost:5000/secure-data`
- **DMZ Service:** `http://localhost:5000/dmz-data`
- **External Service:** `http://localhost:5000/external-data`

Use the OAuth2 token to access the secure data endpoint in the Internal Service.

### Example Requests

1. **Get OAuth2 Token:**

    ```sh
    curl -X POST http://localhost:5000/token -d "client_id=your_client_id&client_secret=your_client_secret&grant_type=client_credentials"
    ```

2. **Access Secure Data (Internal Service):**

    ```sh
    curl -H "Authorization: Bearer your_access_token" http://localhost:5000/secure-data
    ```

## Project Structure
  
  ```sh
  project_root/
  ├── docker-compose.yml
  ├── internal_service/
  │ └── app.py
  ├── dmz_service/
  │ └── app.py
  ├── external_service/
  │ └── app.py
  ├── oauth2_server/
  │ └── app.py
  ├── fluentd/
  │ └── conf/
  │ └── fluentd.conf
  ├── setup_iptables.sh
  ```


## What it Does

- **Network Segmentation:** Uses Docker to create isolated network segments.
- **Strong Authentication:** Implements OAuth2 for token-based authentication and JWT for securing API endpoints.
- **Policy Enforcement:** Uses iptables to enforce strict network policies and prevent lateral movement.
- **Advanced Monitoring:** Utilizes Fluentd for collecting and analyzing logs.

## Contributing

Contributions are welcome! Please fork the repository and use a feature branch. Pull requests are warmly welcome.

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

