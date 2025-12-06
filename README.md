# Stories

A Django-based web application for sharing and reading short stories. Users can create accounts, publish stories, organize them into categories, comment on stories, create reading lists, and follow other authors.

## Features

- **User Authentication**: Email-based registration and login with custom user profiles
- **Story Management**: Create, edit, and publish short stories with rich text content
- **Categories**: Organize stories by genre or theme
- **Comments**: Engage with stories through a commenting system
- **Reading Lists**: Save and organize favorite stories into personal or public lists
- **User Profiles**: Custom profiles with bio, profile pictures, and following/followers
- **Social Features**: Follow other authors and discover new content
- **Responsive Design**: Mobile-friendly interface

## Tech Stack

- **Backend**: Django 5.1.7
- **Database**: SQLite (development), configurable for production
- **Image Processing**: Django ImageKit for profile picture handling
- **Frontend**: HTML, CSS, JavaScript with Bootstrap
- **Deployment**: Ready for deployment on platforms like Heroku, DigitalOcean, etc.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/stories.git
   cd stories
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**:

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (optional, for admin access):

   ```bash
   python manage.py createsuperuser
   ```

## Setup

1. **Environment Variables**: For production, set the following environment variables:
   - `SECRET_KEY`: A secure secret key for Django
   - `DEBUG`: Set to `False` for production
   - `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
   - `DATABASE_URL`: Database connection URL (if using PostgreSQL or other DB)

2. **Static Files**: For production, collect static files:

   ```bash
   python manage.py collectstatic
   ```

3. **Media Files**: Configure your web server to serve media files from the `media/` directory.

## Usage

1. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

2. **Access the application**:
   - Open your browser and go to `http://127.0.0.1:8000/`
   - Register a new account or log in
   - Start creating and reading stories!

## Project Structure

```
stories/
├── accounts/          # User authentication and profiles
├── stories/           # Story management and related models
├── website/           # Static pages and general views
├── templates/         # HTML templates
├── static/            # Static files (CSS, JS, images)
├── django_project/    # Django project settings
├── manage.py          # Django management script
└── requirements.txt   # Python dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you have any questions or issues, please open an issue on GitHub or contact the maintainers.
