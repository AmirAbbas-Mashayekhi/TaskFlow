Ok. I have my MVP API (CS50w Final Project) ready:
Here is what we need to do
This is the current readme file for this project:
# TaskFlow

> "A project manager from hell" - *Pink floyd and coffee* were the main contributors.


#### Video Demo: [Watch Demo](https://youtu.be/6UFRHdf7cs0)

---

## Description

TaskFlow is a powerful project management API designed to streamline team collaboration and task management for software development teams or any other professional groups working on shared projects. It provides comprehensive features such as team management, member invitations, project creation, task management, role assignments, and task commenting. TaskFlow facilitates efficient coordination and communication among team members and is built on robust technologies such as Python, Django Rest Framework (DRF), Celery, and Redis.

### Core Features:
- **Create Teams**: Build teams of users to work collaboratively on projects.
- **Add Members via Invitation**: Invite members to join teams via email.
- **Create Projects**: Organize work into specific projects under a team.
- **Create Tasks**: Break down projects into individual tasks with specific details and deadlines.
- **Comment on Tasks**: Collaborate by allowing team members to comment on task progress and other related issues.
- **Assign Roles to Members**: Ensure accountability by assigning specific roles to team members.

---

## Detailed Workflow

### 1. **Authentication (Auth)**
To interact with the TaskFlow API, the first step for a user is to sign up and authenticate. Authentication in TaskFlow is managed by the Djoser library, which integrates with Django's default user model.

- **Sign Up**: Users can register by making a POST request to /auth/users with their required credentials (username, email, and password).
  
- **JWT Token Generation**: After successful registration, users must obtain a JWT (JSON Web Token) for authentication by making a POST request to /auth/jwt/create with their login credentials. The response will contain a token that the user must attach to all subsequent requests in the request header (Authorization: Bearer <JWT token>). In a full-stack application, this token should be stored in local browser storage or session storage for seamless API interaction.

- **Token Use**: The JWT token is used for authenticating all subsequent API requests, allowing users to interact with teams, projects, and tasks securely.

---

### 2. **User Profile Creation (Participant)**
Once authenticated, the next step is to create a user profile, referred to as a "participant" in the TaskFlow system. This step is crucial as it links the user’s account to their profile, which will be used throughout the application.

- **Register Participant**: The user must provide a valid phone number to create their profile by sending a POST request to /participants/register. This phone number will be verified using a phonenumber verification library, adding an extra layer of security and user validation.

- **Profile Use**: The participant profile allows users to interact with teams and projects, serving as their identity within TaskFlow.

---

### 3. **Teams, Members, Projects, and Tasks**
TaskFlow revolves around team collaboration. Once a participant is registered, they can create teams, invite other members to join, and start managing projects and tasks.

#### **Teams**
- **Create Team**: After profile creation, a user can create a new team by making a POST request to /teams/create. A team represents a group of users collaborating on multiple projects.
  
- **Invite Members**: A team leader can invite other participants to join the team via email. Invitations can be sent through the /teams/invite endpoint, where the recipient receives an invitation link in their email. TaskFlow uses SMTP4Dev for email handling in development environments, while production environments can be configured to use real SMTP servers.

#### **Projects**
- **Create Projects**: A team can work on multiple projects simultaneously. After forming a team, a user can create a project by making a POST request to /projects/create under a specific team. Projects are containers for tasks and can have due dates, descriptions, and other metadata.

#### **Tasks**
- **Create Tasks**: Each project is broken down into tasks. Tasks can be created via the /tasks/create endpoint. Tasks can have titles, descriptions, assignees, due dates, and priorities. Tasks are vital to managing workloads within a project.
  
- **Assign Tasks**: Team leaders can assign tasks to specific team members to ensure accountability and task ownership. This helps distribute work efficiently among team members.

---

### 4. **Task Commenting**
Communication and feedback are critical for completing tasks on time. TaskFlow enables task-level commenting so team members can collaborate and discuss issues related to specific tasks.

- **Comment on Tasks**: Any team member can comment on a task by making a POST request to /tasks/comment. Comments allow for real-time discussions on task progress, issues, and resolutions.

---

### 5. **Role Management**
TaskFlow offers role-based access control, allowing team leaders to assign specific roles to team members.

- **Assign Roles**: Roles such as "Project Manager", "Developer", or "Reviewer" can be assigned to team members to define their responsibilities. This is useful for setting permissions and clarifying each member’s duties.

---

## Background Tasks

TaskFlow is designed with scalability in mind. To handle time-consuming processes, such as sending emails or processing large data sets, TaskFlow uses Celery for background task processing. Redis acts as the message broker for Celery, ensuring that tasks are processed efficiently in the background without slowing down the API response times.

### Example Background Tasks:
- **Sending Invitation Emails**: When a user invites another member to a team, Celery is used to send the email in the background.
- **Reminder Notifications**: Periodic notifications, such as task reminders, can be handled asynchronously by Celery workers.

---

## Technologies Used

TaskFlow is built using the following technologies to ensure reliability, scalability, and performance:

- **Python**: The core language used for the API backend.
- **Django Rest Framework (DRF)**: The primary framework used to build the RESTful API.
- **Djoser**: Handles authentication and token management, simplifying JWT integration.
- **JWT (JSON Web Token)**: Used for securing API endpoints and managing user sessions.
- **Phonenumber Verification Library**: Ensures valid phone numbers are provided during user profile creation.
- **MySQL**: The relational database used for storing user, team, project, and task data.
- **Redis**: Used as a message broker for background tasks and caching.
- **SMTP4Dev**: A local SMTP server for testing email functionality in development environments.
- **Celery**: Handles background tasks, ensuring long-running processes don’t block API responses.

And this is from cs50w website:
Designing and implementing a web application of your own with Python and JavaScript.
Overview

The final project is your opportunity to design and implement a dynamic website of your own. So long as your final project draws upon this course’s lessons, the nature of your website will be up to you, subject to some constraints as indicated below.
Requirements

In this project, you are asked to build a web application of your own. The nature of the application is up to you, subject to a few requirements:

    Your web application must be sufficiently distinct from the other projects in this course (and, in addition, may not be based on the old CS50W Pizza project), and more complex than those.
        A project that appears to be a social network is a priori deemed by the staff to be indistinct from Project 4, and should not be submitted; it will be rejected.
        A project that appears to be an e-commerce site is strongly suspected to be indistinct from Project 2, and your README.md file should be very clear as to why it’s not. Failing that, it should not be submitted; it will be rejected.
    Your web application must utilize Django (including at least one model) on the back-end and JavaScript on the front-end.
    Your web application must be mobile-responsive.

The most common cause for failure of the final project is not spending enough effort on this next instruction. Read it completely. Your README.md file should be minimally multiple paragraphs in length, and should provide a comprehensive documentation of what you did and, if applicable, why you did it. Ensure you allocate sufficient time and energy to writing a README.md that you are proud of and that documents your project thoroughly, and that distinguishes this project from others in the course and defends its complexity. Simply saying, effectively, “It’s different from the other projects and it was complex to build.” is not at all sufficient justification of distinctiveness and complexity. This section alone should consist of several paragraphs, before you even begin to talk about the documentation of your project.

    In a README.md in your project’s main directory, include a writeup describing your project, and specifically your file MUST include all of the following:
        Under its own header within the README called Distinctiveness and Complexity: Why you believe your project satisfies the distinctiveness and complexity requirements, mentioned above.
        What’s contained in each file you created.
        How to run your application.
        Any other additional information the staff should know about your project.
    If you’ve added any Python packages that need to be installed in order to run your web application, be sure to add them to a requirements.txt file!
    Though there is not a hard requirement here, a README.md in the neighborhood of 500 words is likely a solid target, assuming the other requirements are also satisfied.

Failure to adhere to these requirements WILL result in a failing grade for the project, and you will need to wait and resubmit.

Beyond these requirements, the design, look, and feel of the website are up to you!
How to Submit

    Visit this link, log in with your GitHub account, and click Authorize cs50. Then, check the box indicating that you’d like to grant course staff access to your submissions, and click Join course.
    Install Git and, optionally, install submit50.

When you submit your project, the structure of your web50/projects/2020/x/capstone branch should match, in general, the file structure of Projects 1, 2, 3, and 4. Your branch should also not contain any code from any other projects, only this one. Failure to adhere to this file structure will likely result in your submission being rejected.

Your README.md file must also be at the highest level of your project. That is to say it should exist at https://github.com/me50/USERNAME/blob/web50/projects/2020/x/capstone/README.md (where USERNAME is your own GitHub username as provided in the form, below). If it doesn’t, reorganize your repository as needed to match this paradigm.

    If you’ve installed submit50, execute

    submit50 web50/projects/2020/x/capstone

    Otherwise, using Git, push your work to https://github.com/me50/USERNAME.git, where USERNAME is your GitHub username, on a branch called web50/projects/2020/x/capstone.
    Record a screencast not to exceed 5 minutes in length (and not uploaded more than one month prior to your submission of this project), in which you demonstrate your project’s functionality. Be certain that every requirement of the specification, above, is demonstrated in your video. There’s no need to show your code in this video, just your application in action; we’ll review your code on GitHub. Upload that video to YouTube (as unlisted or public, but not private) or somewhere else. Do not submit a YouTube “short”.
    Submit this form.

You can then go to https://cs50.me/cs50w to view your current progress!

On 6 January 2025, our gradebooks were “reset”, for cleanup and organization purposes. All work submitted and graded in 2024 will remain archived, and you should never re-submit work on which you previously earned a passing grade. If your course is incomplete at the time of the gradebook reset, not to worry. Simply continue where you left off, and your older scores will import once any newly-submitted work is graded in 2025!

As you can see my projects lacks that frontend part a little (I mean the API is browsable and has a UI)


Look carefully at how they want the readme to be. How there is a very important section for explaining the distinctivness and complexity.

I need you to create a readme that covers all the factors that cs50w has in mind from a readme file and also I need you to very gracefully explain why I decided to focus only on the backend.
Primarly because this is a very complex project and goes beyond the scope of the course so the frontend would also be outside the scope. and also i specialize in backend so this is kinda understandable. just please try to win the teacher over with the words.

Also add every detail they expect like how to run the application, and .... (Everything) THIS IS VERY IMPORTANT

NOW GENERATE THE README AND KEEP IN MIND THAT THE APP IS NOW DOCKERIZED WITH DOCKER COMPOSE