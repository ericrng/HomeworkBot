# HomeworkBot
****
## What is HomeworkBot?
**HomeworkBot** is a Discord Bot built for **School Discord Servers**. Its purpose is to be a **better to-do list** for **students**.
## Current Functions
HomeworkBot is still an active project and still in development, though most major functions have been completed.  
Admins have their 6 commands below in order to set up the bot and prevent mischief.  
Non-admin commands (Homework Commands) are public-access and can be used by anyone.
### Admin Commands
- #### /insert_class_periods
- #### /insert_class_names
- #### /insert_teacher_names
- #### /remove_periods
- #### /remove_class_names
- #### /remove_teacher_names
### Homework Commands
- #### /show_class_periods
- #### /show_class_names
- #### /show_teacher_names
- #### /show_homework 
- #### /show_schedule
- #### /add_homework
- #### /remove_homework
- #### /remove_from_schedule
- #### /change_homework_status
- #### /insert_into_schedule
- #### /settings
- #### /change_settings
## Future Functions
HomeworkBot is, as mentioned previously, a WIP. Features will be added as suggestions come in and changes to the codebase will be done as well.
### Planned Features  
* ~~Syncing whenever a Homework is added.~~
* ~~Syncing as an optional setting for users.~~
* ~~Automatically deleting Homework that is past-due.~~
* ~~Sending multiple embeds to circumvent maximum embed field limits.~~ 
### Other Potential Additions
* Reliability Scores for syncers. (Basically, people are graded on how good their syncs are)
* Using a Reliability Score as a filter. (Allowing users to limit who they get their syncs from)


## How to Setup?
1. ### Install Dependencies
   **In your terminal, do:**
    >    pip install -r requirements.txt   

    This downloads the dependencies.
2. ### Create a .env file
    Simply create a file named .env and enter in your details.  
    > DISCORD_TOKEN="INSERT YOUR TOKEN HERE"  
   > DATABASE="INSERT YOUR DATABASE HERE"  
   > USERNAME="INSERT YOUR USERNAME HERE"  
   > HOST="INSERT YOUR HOSTNAME HERE"  
   > PASSWORD="INSERT YOUR PASSWORD HERE"  
   > AUTHORIZED_USER="INSERT YOUR USER ID HERE"  
    
    Fill out all of these fields with your specific information.  
    Token is your bot token and Authorized User is your Discord User ID.  
    Everything else is database details to connect to your database. 
3. ### Enter whatever you want into periods, classes, and teacher names.
    That is all the bot setup done! Now you can run the program, go on Discord and start entering stuff in.