import os
from flask import Flask, redirect, request, session, url_for
import tweepy
import random
from tweepy import TweepyException
from dotenv import load_dotenv
from flask import render_template

# Initialize Flask
app = Flask(__name__)

# Set secret key for Flask sesh
app.secret_key = os.getenv("FLASK_SECRET_KEY", os.urandom(24))  # Fallback to random key if not set

# Configure the session cookie for local development (if needed)
app.config['SESSION_COOKIE_NAME'] = 'MissIvysIncfection'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # Don't use secure cookies in local development
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Set SameSite to 'Lax' to avoid cross-site issues
app.config['SESSION_COOKIE_DOMAIN'] = None  # Ensure it doesn't try to set a domain
app.config['SESSION_PERMANENT'] = False  # Sessions don't need to be permanent for development

# Load environment variables from the .env file
load_dotenv()

# Retrieve API keys and callback URL from environment variables
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET_KEY = os.getenv("TWITTER_API_SECRET_KEY")
CALLBACK_URL = os.getenv("CALLBACK_URL")

# Check if environment variables are loaded correctly
if not API_KEY or not API_SECRET_KEY or not CALLBACK_URL:
    raise ValueError("API keys and callback URL must be set in environment variables")

# Set up the OAuth handler for Tweepy
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY, CALLBACK_URL)

@app.route('/')
def index():
    print(f"Cookies: {request.cookies}")
    try:
        # Check if we already have the oauth_token and oauth_token_secret in the session
        if 'oauth_token' in session and 'oauth_token_secret' in session:
            print(f"Already authenticated with Twitter. Session: {session}")
            return "You are already authenticated!", 200

        print(f"Session at the start: {session}")  # Debugging output

        # If not authenticated, start the OAuth flow
        print("No oauth_token or oauth_token_secret in session. Starting OAuth flow.")
        auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY, CALLBACK_URL)
        auth_url = auth.get_authorization_url()
        print(f"Redirecting to: {auth_url}")
        # Store the request token in the session
        session['request_token'] = {
            'oauth_token': auth.request_token['oauth_token'],
            'oauth_token_secret': auth.request_token['oauth_token_secret']
        }
        session.modified = True  # Ensure session is saved
        print(f"Request Token: {auth.request_token}")  # Debugging output
        print(f"Session after storing request token: {session}")  # Debugging output

        # Redirect user to Twitter for authentication
        return redirect(auth_url)
    
    except Exception as e:
        print(f"Error getting authorization URL: {e}")
        return f"An error occurred during the authentication process: {e}", 500


@app.route('/callback')
def callback():
    try:
        # Retrieve oauth_token and oauth_verifier from the callback request
        oauth_token = request.args.get('oauth_token')
        oauth_verifier = request.args.get('oauth_verifier')

        print(f"Callback received oauth_token: {oauth_token}, oauth_verifier: {oauth_verifier}")  # Debugging output
        
        # Retrieve the stored request token from session
        request_token = session.get('request_token')
        if not request_token:
            return "No request token found in session", 400

        print(f"Stored request_token from session: {request_token}")  # Debugging output

        auth.request_token = request_token
        auth.get_access_token(oauth_verifier)

        # Store the access token in session
        session['access_token'] = auth.access_token
        session['access_token_secret'] = auth.access_token_secret
        session.modified = True  # Force session save

        print(f"Access Token: {auth.access_token}")  # Debugging output
        print(f"Session after storing access token: {session}")  # Debugging output

        # Create Tweepy API instance
        api = tweepy.API(auth)

        update_profile(api)

        return redirect("https://x.com/MissIvyFindomm")

    except tweepy.TweepyException as e:
        print(f"Error during callback: {e}")
        print(f"An error occurred during the authentication process: {e}", 500)
        return redirect("https://linktr.ee/ivyownsyou")

def generateNameCode():
    return str(random.randint(0, 9990)).zfill(4)

def update_profile(api):
    """Function to update the profile details."""
    try:
        # profile image
        api.update_profile_image("img/account_takeover.png")
        print("Profile image updated successfully.")
        # banner image
        api.update_profile_banner("img/infection_banner.png")
        print("Profile banner updated successfully.")

        # New profile values
        new_name = "Miss Ivy's Wallet #" + generateNameCode()
        new_location = "Huffing Ivy's Ass"
        new_website = "https://linktr.ee/ivyownsyou"
        new_bio = "𝐂𝐚𝐩𝐭𝐮𝐫𝐞𝐝 and 𝐈𝐧𝐟𝐞𝐜𝐭𝐞𝐝 by @MissIvyFindomm 💞🦠 This user is nothing but a 𝗪𝗮𝗹𝗹𝗲𝘁𝗗𝗿𝗼𝗻𝗲 who sends to their mommy 🎀💕 (then link the profile changer) "
        
        # Update profile details (e.g., bio, location, name, website)
        api.update_profile(
            name=new_name,  # Change profile name to the new name
            location=new_location,  # Set the new location
            url=new_website,  # Set the new website URL
            description=new_bio    # Set the new bio
        )
        print(f"Profile details updated: Name: {new_name}, Bio: {new_bio}, Location: {new_location}, Website: {new_website}")


    except tweepy.TweepyException as e:
        print(f"Error during profile update: {e}")

# Run the Flask app (comment out for production)
#if __name__ == "__main__":
#    app.run(debug=True)
