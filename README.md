# Django Task Manager

A web application for managing tasks, projects, tags, and user accounts.

## Features

- User registration, login, and profile management
- Task creation, editing, deletion, and tagging
- Project management
- Commenting on tasks
- Tag filtering and clickable tags
- Signals for sending emails on user, project, and task creation
- Management commands for bulk user creation and task notifications
- Pytest support for testing

## Setup

1. **Clone the repository**

   ```sh
   git clone <your-repo-url>
   cd <your-project-folder>
   ```

2. **Create and activate a virtual environment**

   ```sh
   python -m venv env
   env\Scripts\activate  # On Windows
   ```

3. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

4. **Apply migrations**

   ```sh
   python manage.py migrate
   ```

5. **Create a superuser (admin)**

   ```sh
   python manage.py createsuperuser
   ```

6. **Run the development server**

   ```sh
   python manage.py runserver
   ```

7. **Run tests with pytest**

   ```sh
   pytest
   ```

## Custom Management Commands

- **Create 10 users:**
  ```sh
  python manage.py create_ten_users
  ```
- **Send notifications for tasks due tomorrow:**
  ```sh
  python manage.py notify_upcoming_tasks
  ```

## Email

- By default, emails are printed to the console.  
  Configure your email backend in `settings.py` for production use.

## Project Structure

- `accounts/` – User management, registration, signals
- `tasks/` – Task, project, tag management, signals, commands
- `templates/` – HTML templates for all pages

## Testing

- Tests are written using `pytest` and `pytest-django`.
- Test files are located in `accounts/tests/` and `tasks/tests/`.

## License

MIT License

---

**Enjoy managing your tasks!**