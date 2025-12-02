# Admin Tattler archiver

[Admin Tattler is a Devvit app on Reddit](https://developers.reddit.com/apps/admin-tattler) that sends a message to the moderators of subreddits it is installed on when a Reddit admin removes something from their subreddit. It can also send a notification to Slack or Discord.

This script looks for any unarchived messages sent from /u/admin-tattler, and archives those mod messages.

### .env

```
# Reddit
REDDIT_CLIENT_ID     =
REDDIT_CLIENT_SECRET =
REDDIT_USER_AGENT    =
REDDIT_REFRESH_TOKEN =
```
