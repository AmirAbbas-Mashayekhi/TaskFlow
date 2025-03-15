# TaskFlow

> "A project manager from hell" - *Pink Floyd and coffee* were the main contributors.

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

## Distinctiveness and Complexity

### Distinctiveness
TaskFlow is distinct from other projects in this course due to its focus on backend development and the comprehensive set of features it offers for project management. Unlike a social network or an e-commerce site, TaskFlow is designed to facilitate team collaboration and task management, which involves complex interactions between users, teams, projects, and tasks. The use of Celery for background task processing and Redis as a message broker further distinguishes this project from others.

### Complexity
The complexity of TaskFlow lies in its robust backend architecture, which includes:
- **Django Rest Framework (DRF)**: Used to build a RESTful API that supports various operations such as user authentication, team management, project creation, task management, and role assignments.
- **Djoser**: Handles authentication and token management, simplifying JWT integration.
- **Celery**: Manages background tasks, ensuring that time-consuming processes like sending emails and processing large data sets do not block API responses.
- **Redis**: Acts as a message broker for Celery, ensuring efficient task processing.
- **Docker and Docker Compose**: The application is containerized, making it easy to deploy and manage.

The decision to focus solely on the backend was made to ensure that the project remains within the scope of the course while still demonstrating a high level of complexity and functionality. As a backend specialist, I aimed to create a robust and scalable API that can be easily integrated with any frontend framework in the future.

---

## Detailed Workflow

### 1. **Authentication (Auth)**
To interact with the TaskFlow API, the first step for a user is to sign up and authenticate. Authentication in TaskFlow is managed by the Djoser library, which integrates with Django's default user model.

- **Sign Up**: Users can register by making a POST request to `/auth/users` with their required credentials (username, email, and password).
  
- **JWT Token Generation**: After successful registration, users must obtain a JWT (JSON Web Token) for authentication by making a POST request to `/auth/jwt/create` with their login credentials. The response will contain a token that the user must attach to all subsequent requests in the request header (Authorization: Bearer `<JWT token>`). In a full-stack application, this token should be stored in local browser storage or session storage for seamless API interaction.

- **Token Use**: The JWT token is used for authenticating all subsequent API requests, allowing users to interact with teams, projects, and tasks securely.

---

### 2. **User Profile Creation (Participant)**
Once authenticated, the next step is to create a user profile, referred to as a "participant" in the TaskFlow system. This step is crucial as it links the user’s account to their profile, which will be used throughout the application.

- **Register Participant**: The user must provide a valid phone number to create their profile by sending a POST request to `/participants/register`. This phone number will be verified using a phonenumber verification library, adding an extra layer of security and user validation.

- **Profile Use**: The participant profile allows users to interact with teams and projects, serving as their identity within TaskFlow.

---

### 3. **Teams, Members, Projects, and Tasks**
TaskFlow revolves around team collaboration. Once a participant is registered, they can create teams, invite other members to join, and start managing projects and tasks.

#### **Teams**
- **Create Team**: After profile creation, a user can create a new team by making a POST request to `/teams/create`. A team represents a group of users collaborating on multiple projects.
  
- **Invite Members**: A team leader can invite other participants to join the team via email. Invitations can be sent through the `/teams/invite` endpoint, where the recipient receives an invitation link in their email. TaskFlow uses SMTP4Dev for email handling in development environments, while production environments can be configured to use real SMTP servers.

#### **Projects**
- **Create Projects**: A team can work on multiple projects simultaneously. After forming a team, a user can create a project by making a POST request to `/projects/create` under a specific team. Projects are containers for tasks and can have due dates, descriptions, and other metadata.

#### **Tasks**
- **Create Tasks**: Each project is broken down into tasks. Tasks can be created via the `/tasks/create` endpoint. Tasks can have titles, descriptions, assignees, due dates, and priorities. Tasks are vital to managing workloads within a project.
  
- **Assign Tasks**: Team leaders can assign tasks to specific team members to ensure accountability and task ownership. This helps distribute work efficiently among team members.

---

### 4. **Task Commenting**
Communication and feedback are critical for completing tasks on time. TaskFlow enables task-level commenting so team members can collaborate and discuss issues related to specific tasks.

- **Comment on Tasks**: Any team member can comment on a task by making a POST request to `/tasks/comment`. Comments allow for real-time discussions on task progress, issues, and resolutions.

---

### 5. **Role Management**
TaskFlow offers role-based access control, allowing team leaders to assign specific roles to team members.

- **Assign Roles**: Roles such as "Project Manager", "Developer", or "Reviewer" can be assigned to team members to define their responsibilities. This is useful for setting permissions and clarifying each member’s duties.

---

## Permissions

TaskFlow uses custom permissions to ensure that only authorized users can perform certain actions. The permissions are defined in the `tasks/permissions.py` file.

- **IsRegisteredParticipant**: Ensures that the user is a registered participant.
- **IsNotRegisteredParticipant**: Ensures that the user is not a registered participant.

```py
// filepath: /home/amir/CS50w/TaskFlow/tasks/permissions.py
from rest_framework.permissions import BasePermission
from .models import Participant

class IsRegisteredParticipant(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and Participant.objects.filter(user_id=request.user.id).exists()
        )

class IsNotRegisteredParticipant(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and not Participant.objects.filter(user_id=request.user.id).exists()
        )
```

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
- **Docker and Docker Compose**: Used for containerizing the application, making it easy to deploy and manage.

---

## How to Run the Application

### Prerequisites
- Docker
- Docker Compose

### Steps to Run
1. **Clone the Repository**:
    ```sh
    git clone https://github.com/yourusername/TaskFlow.git
    cd TaskFlow
    ```

2. **Set Up Environment Variables**:
    Create a `.env` file in the root directory and add the necessary environment variables:
    ```env
    DJANGO_SECRET_KEY=your_secret_key
    MYSQL_ROOT_PASSWORD=root_password
    MYSQL_DATABASE=taskflow
    MYSQL_USER=user
    MYSQL_PASSWORD=password
    ```

3. **Build and Run the Docker Containers**:
    ```sh
    docker-compose up --build
    ```

4. **Apply Migrations**:
    ```sh
    docker-compose exec backend python manage.py migrate
    ```

5. **Create a Superuser**:
    ```sh
    docker-compose exec backend python manage.py createsuperuser
    ```

6. **Access the Application**:
    Open your browser and go to `http://localhost:8000`.

---

## File Structure

- `TaskFlowAPI/`: Contains the Django project files.
- `Dockerfile`: Docker configuration for the backend service.
- `docker-compose.yml`: Docker Compose configuration for the entire application.
- `requirements.txt`: List of Python packages required for the project.
- `.env`: Environment variables for the project.
- `README.md`: Project documentation.

---

## Additional Information

- The application is designed to be easily extendable with a frontend framework.
- The backend API is fully documented and browsable, making it easy to integrate with any frontend.
- The use of Docker ensures that the application can be deployed consistently across different environments.

---

By focusing on the backend, I aimed to create a robust and scalable API that can be easily integrated with any frontend framework in the future. This approach not only demonstrates the complexity and functionality of the project but also aligns with my specialization in backend development.
