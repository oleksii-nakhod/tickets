# Railroad System
## Quickstart
This code is hosted [here](https://tickets.wartexnik.com).  
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
git clone https://github.com/konovaliuk/Nakhod_Railroad.git
pip install -r requirements.txt
```
2. Initialize a database. For MySQL, you can use the [sample file](init_database.sql).
```
mysql> source init_database.sql
```
3. Register a [Stripe](https://dashboard.stripe.com) developer account to get an API and endpoint keys.
4. Rename .env.example to .env, replace sample environment variables.
5. Start the server.
```
python app.py
```