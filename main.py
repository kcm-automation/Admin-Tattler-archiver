from dotenv import load_dotenv
import logging
import os
import praw

# Load .env before using any environment variables
if not os.environ.get("NOT_DOTENV"):
    load_dotenv()
    print(".env was loaded.")

DEFAULT_LOG_LEVEL = "DEBUG"
LOG_LEVEL = os.environ.get("LOG_LEVEL", DEFAULT_LOG_LEVEL)
if LOG_LEVEL not in logging._nameToLevel:
    raise RuntimeError(f"Invalid LOG_LEVEL={LOG_LEVEL}")

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=LOG_LEVEL
)

def reddit_client():
    reddit_client = praw.Reddit(
        client_id     = os.getenv('REDDIT_CLIENT_ID'),
        client_secret = os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent    = os.getenv('REDDIT_USER_AGENT'),
        refresh_token = os.getenv('REDDIT_REFRESH_TOKEN'),
    )

    try:
        me = reddit_client.user.me()
        logging.info(f"Successfully authenticated")
        return reddit_client
    except Exception as e:
        logging.error(f"Refresh token failed: {e}")
        raise RuntimeError(f"Refresh token failed: {e}")

def main():
    reddit = reddit_client()
    subreddit = reddit.subreddit("UkrainianConflict")

    logging.info("Fetching unarchived modmails...")
    modmails = subreddit.modmail.conversations(state='all')

    # count number of modmails
    modmails = list(modmails)
    logging.info(f"Got {len(modmails)} modmail(s).")

    # For each message in modmails
    for conversation in modmails:
        logging.info(f"Modmail ID: {conversation.id}. State: {conversation.state}")

        first_message = conversation.messages[0]
        first_author = first_message.author.name

        # If admin tattler
        if (
            first_author.lower() == "admin-tattler"
            and conversation.subject == "Admin Action Detected"
        ):

            try:
                # Leave a private mod note
                conversation.reply(body="_Archived by a [script](https://github.com/kcm-automation/Admin-Tattler-archiver)._", internal=True)

                # archive it
                conversation.archive()
                logging.info("Conversation was archived")
                
            except Exception as e:
                logging.error(f"Error during processing: {e}")

        else:
            logging.info("└ Modmail not from admin-tattler. Skipping...")


if __name__ == "__main__":
    main()
