# README
### INSTALLATION AND DEPLOYMENT:

In order for this program to work, you will need to install a few items.
All of these items are listed in the Pipfile.

We've created a makefile to ease in the deployment of our site, however
There are two additional environment variables that are included in the submission on canvas.
Move the app-env file into the bloodsite directory to ensure these variables are present on deployment.

Simply enter the bloodsite directory and type make. A menu will appear to guide you.

After the site is deployed visit http://127.0.0.1:5000/ in the browser of your choice.
### USE:

The site will launch at a homepage, where you can register an account.

The idea behind our project is an internal website for a series of blood banks.
The users are employees of the blood bank. You are an employee so you may register an account, and following that log in with your new account.

As an employee you will be creating donors, updating the bank with donations or withdraws, and updating new branches. 
We have loaded the database with entries to create an ease of use.

### DISCLAIMERS:

Some of the permissions that the employee has over the accounts as well as the banks,
such as creating their own profile, branch of the bank, among others would be reserved for an administrator or manager.
For ease of use for the grader we've enacted no such restrictions. 
