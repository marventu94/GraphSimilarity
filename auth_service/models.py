class User:
    def __init__(self, username, password, subscription_type):
        self.username = username
        self.password = password
        self.subscription_type = subscription_type

# Simulated user database
users_db = {
    "freemium_user": User("freemium_user", "password123", "FREEMIUM"),
    "premium_user": User("premium_user", "password456", "PREMIUM")
}
