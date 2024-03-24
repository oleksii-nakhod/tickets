# Railroad System
## Quickstart
This code is hosted [here](https://tickets.nakhod.me).  
To test the main functionality, follow these steps:
1. Sign up for an account.
2. Search for Kyiv-Dnipro trains on 27.03.2023.
3. During payment, input the card number 4242 4242 4242 4242, any expiry date in the future, and any three-digit CVC ([Stripe docs](https://stripe.com/docs/testing) for reference).
## Self-hosting
> **Note**  
> You will need a publicly accessible URL so that Stripe can send a confirmation of a successful payment.

To host the code yourself, follow these steps:
1. Clone the repository and install the dependencies.
```
git clone https://github.com/oleksii-nakhod/tickets.git
pip install -r requirements.txt
```
2. Initialize a database. For MySQL, you can use the [sample file](init_database.sql).
```
mysql> source init_database.sql
```
3. Install `wkhtmltopdf`
```
sudo apt install -y wkhtmltopdf
```
4. Register a [Stripe](https://dashboard.stripe.com) developer account to get an API and endpoint keys.
5. Register a [SendGrid](https://app.sendgrid.com) developer account to get an API key.
6. Rename the file `.env.example` to `.env`, replace sample environment variables.
7. Start the server.
```
python app.py
```
## Acknowledgements
- Icons from [Flaticon](https://www.flaticon.com/authors/freepik)