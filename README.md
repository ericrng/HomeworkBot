# HomeworkBot
****
## What is HomeworkBot?
**HomeworkBot** is a Discord Bot built for **School Discord Servers**. Its purpose is to be a **better to-do list** for **students**.  
**Made with Psycopg and Discord.py.** 
## Current Commands
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
- #### /help
## Current Features
### Settings
Settings are viewable via /settings and changeable /change_setings. (All settings are false by default)
- #### Auto-Sync:
   > Auto-Sync adds homework when you and someone else have the same schedule. (If the class, teacher, and period match in specific.)  
   > If you have Auto-Sync on and the other person adds homework, you will have the same homework added automatically. 
- #### Auto-Delete:
   > Auto-Delete deletes any homeworks that are past due (the due date is in the past).
- #### Visibility Settings:
   > Visibility Settings changes the ephemeral status of certain messages.
   > It does not change the ephemeral status for non-show commands except for settings.
## Future Functions
HomeworkBot is a WIP. Features will be added as suggestions come in and changes to the codebase will be done as well.
### Planned Features  
* ~~Syncing whenever a Homework is added.~~
* ~~Syncing as an optional setting for users.~~
* ~~Automatically deleting Homework that is past-due.~~
* ~~Sending multiple embeds to circumvent maximum embed field limits.~~ 
* ~~Adding Visibility Options~~
* Sending messages when homework is due.
* Adding a feature that allows you to change whether you get a message or not for due homework. 
* Adding Homework via unique id's for class name and teacher name. 
### Other Potential Additions
* Reliability Scores for syncers. (Basically, people are graded on how good their syncs are)
* Using a Reliability Score as a filter. (Allowing users to limit who they get their syncs from)


## How to Set up?
1. ### Install Dependencies
   **In your terminal, do:**
    >    pip install -r requirements.txt   

    This downloads the dependencies.
2. ### Create a .env file
    Simply create a file named .env and enter in your details.  
    You can either use the parameters for a connection or simply use the database url. 
    > DISCORD_TOKEN="INSERT YOUR TOKEN HERE"  
   > DATABASE="INSERT YOUR DATABASE HERE"  
   > USERNAME="INSERT YOUR USERNAME HERE"  
   > HOST="INSERT YOUR HOSTNAME HERE"  
   > PASSWORD="INSERT YOUR PASSWORD HERE"  
   > AUTHORIZED_USER="INSERT YOUR USER ID HERE"  
   > DB_URL="INSERT YOUR DB_URL HERE" 
    
    Fill out all of these fields with your specific information.  
    Token is your bot token and Authorized User is your Discord User ID.  
    Everything else is database details to connect to your database. 
3. ### Enter whatever you want into periods, classes, and teacher names.
    That is all the bot setup done! Now you can run the program, go on Discord and start entering stuff in.