# IPO Alert

IPO Alert is an application that scrapes data from the web about upcoming and recently available IPOs in Nepal and sends email alerts to a list of individual email addresses.

## Features

- Scrapes data from the web about upcoming and recently available IPOs in Nepal
- Sends email alerts to a list of individual email addresses
- Runs daily at 10 AM NST and sends alerts if there is an IPO opening date that matches today's date

## Setup

1. Clone the repository and navigate to the project directory.
2. Install the required dependencies by running `pip install requirements.txt`.
3. Create a `.env` file in the project root and add copy the contents of `.env.reference` file:
    - `EMAIL`: The email address to use for sending alerts.
    - `PASSWORD`: The password for the email address.
    - `RECEIVERS`: A comma-separated list of email addresses to send alerts to.
4. Run the application by running `python main.py`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you would like to contribute.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
