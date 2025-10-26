import boto3
from werkzeug.security import generate_password_hash, check_password_hash
from botocore.exceptions import ClientError
import logging

class AuthManager:
    def __init__(self, region, aws_access_key_id, aws_secret_access_key, aws_session_token, table_name):
        self.dynamodb = boto3.resource(
            'dynamodb',
            region_name=region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token
        )
        self.table_name = table_name
        self.table = self.dynamodb.Table(table_name)

    def register_user(self, username, email, password):
        """
        Register a new user by saving their username, email, and hashed password to DynamoDB.
        """
        hashed_password = generate_password_hash(password)

        try:
            # Save the new user to the DynamoDB table
            response = self.table.put_item(
                Item={
                    'username': username,
                    'email': email,
                    'password': hashed_password
                }
            )
            logging.info(f"User {username} registered successfully.")
            return True
        except ClientError as e:
            logging.error(f"Error registering user {username}: {e}")
            return False

    def authenticate_user(self, username, password):
        """
        Authenticate a user by comparing the provided password with the hashed password stored in DynamoDB.
        """
        try:
            # Fetch user data from DynamoDB
            response = self.table.get_item(Key={'username': username})
            user = response.get('Item')
            
            if user and check_password_hash(user['password'], password):
                logging.info(f"User {username} authenticated successfully.")
                return True
            else:
                logging.warning(f"Authentication failed for user {username}.")
                return False
        except ClientError as e:
            logging.error(f"Error authenticating user {username}: {e}")
            return False

    def change_password(self, username, old_password, new_password):
        """
        Change the password for an existing user after verifying the old password.
        """
        try:
            # Fetch user data from DynamoDB
            response = self.table.get_item(Key={'username': username})
            user = response.get('Item')

            if user and check_password_hash(user['password'], old_password):
                # Update password if old password is correct
                new_hashed_password = generate_password_hash(new_password)
                self.table.update_item(
                    Key={'username': username},
                    UpdateExpression="SET password = :new_password",
                    ExpressionAttributeValues={':new_password': new_hashed_password}
                )
                logging.info(f"Password for user {username} changed successfully.")
                return True
            else:
                logging.warning(f"Password change failed for user {username}: incorrect old password.")
                return False
        except ClientError as e:
            logging.error(f"Error changing password for user {username}: {e}")
            return False

    def delete_user(self, username):
        """
        Delete a user from the DynamoDB table.
        """
        try:
            self.table.delete_item(Key={'username': username})
            logging.info(f"User {username} deleted successfully.")
            return True
        except ClientError as e:
            logging.error(f"Error deleting user {username}: {e}")
            return False
