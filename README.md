# BlogBreeze 🚀

A modern, feature-rich Django blog platform with Azure cloud integration, rich text editing, and responsive design.

## 🌐 Live Demo

**Production**: [https://blogbreeze-arfcaubvgqbmejg0.eastasia-01.azurewebsites.net](https://blogbreeze-arfcaubvgqbmejg0.eastasia-01.azurewebsites.net)

## ✨ Features

### Core Functionality
- 📝 Rich text editor (CKEditor) with code syntax highlighting
- 🖼️ Image upload with Azure Blob Storage integration
- 🏷️ Categories and tags for content organization
- 💬 Comment system with moderation
- 🔍 Full-text search functionality
- 👤 User authentication and profiles
- 📱 Fully responsive design with dark mode support

### User Roles
- **Admin**: Full access to all features
- **Author**: Create, edit, and publish posts
- **Reader**: View posts and leave comments

### Technical Features
- ⚡ Azure App Service deployment
- 🗄️ PostgreSQL database with Azure integration
- 📦 Azure Blob Storage for media files
- 🔄 GitHub Actions CI/CD pipeline
- 🎨 Modern UI with Tailwind CSS
- 🔒 Secure authentication and authorization

## 🛠️ Tech Stack

- **Backend**: Django 5.2.8
- **Database**: PostgreSQL 14 (Azure)
- **Storage**: Azure Blob Storage
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Editor**: CKEditor 6
- **Deployment**: Azure App Service
- **CI/CD**: GitHub Actions

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL (for local development)
- Azure account (for production)
- Git

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Younas-29/BlogBreeze.git
   cd BlogBreeze
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Frontend: http://127.0.0.1:8000
   - Admin: http://127.0.0.1:8000/admin

## ☁️ Azure Deployment

### Infrastructure

The application is deployed on Azure with the following resources:

- **App Service**: `blogbreeze` (Python 3.11)
- **PostgreSQL**: `blogbree-server` (Flexible Server)
- **Storage Account**: `bbstorage2025` (Blob Storage)
- **Redis Cache**: `blogbree-cache` (for caching)
- **Virtual Network**: `blogbreezeVnet` (private networking)

### Automatic Deployment

The project uses GitHub Actions for CI/CD. Every push to the `azd-enable-copilot-coding-agent-with-azure` or `main` branch automatically:

1. Installs dependencies
2. Collects static files
3. Deploys to Azure App Service
4. Runs database migrations
5. Starts the application

### Manual Deployment

To deploy manually:

```bash
# Login to Azure
az login

# Deploy
az webapp up --name blogbreeze --resource-group Blogbreeze
```

## 📁 Project Structure

```
BlogBreeze/
├── accounts/           # User authentication and profiles
├── blog/              # Core blog functionality
│   ├── models.py      # Post, Category, Tag, Comment models
│   ├── views.py       # Blog views
│   ├── forms.py       # Blog forms
│   └── admin.py       # Admin configuration
├── BlogBreeze/        # Project settings
│   ├── settings.py    # Django settings
│   ├── urls.py        # URL configuration
│   └── wsgi.py        # WSGI configuration
├── templates/         # HTML templates
├── static/           # Static files (CSS, JS, images)
├── media/            # User-uploaded files (local dev)
├── .github/          # GitHub Actions workflows
├── requirements.txt  # Python dependencies
├── startup.sh        # Azure startup script
└── manage.py         # Django management script
```

## 🔧 Configuration

### Environment Variables

#### Required for Production:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `AZURE_POSTGRESQL_HOST`: PostgreSQL server hostname
- `AZURE_POSTGRESQL_DATABASE`: Database name
- `AZURE_POSTGRESQL_USER`: Database user
- `AZURE_POSTGRESQL_PASSWORD`: Database password
- `AZURE_ACCOUNT_NAME`: Storage account name
- `AZURE_ACCOUNT_KEY`: Storage account key
- `AZURE_CONTAINER`: Blob container name (default: `media`)

#### Optional:
- `CSRF_TRUSTED_ORIGINS`: Trusted origins for CSRF
- `AZURE_REDIS_CONNECTIONSTRING`: Redis connection string

## 🧪 Testing

Run tests:
```bash
python manage.py test
```

## 📝 Usage

### Creating a Blog Post

1. Login to the admin panel or user dashboard
2. Click "Create Post"
3. Fill in the title, content, category, and tags
4. Upload a featured image (optional)
5. Choose "Draft" or "Published" status
6. Click "Save"

### Managing Categories and Tags

Categories and tags can be managed through:
- Admin panel: `/admin`
- User dashboard (for authors and admins)

### Comment Moderation

Comments can be moderated through the admin panel. Set `is_approved=True` to approve comments.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## � LiceTnse

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## � Authorsd

- **Younas Khan** - [GitHub](https://github.com/Younas-29)

## 🙏 Acknowledgments

- Django framework
- Azure cloud platform
- CKEditor team
- Tailwind CSS
- All contributors

## 📞 Support

For support, email your-email@example.com or open an issue in the GitHub repository.

## 🔗 Links

- **Repository**: https://github.com/Younas-29/BlogBreeze
- **Live App**: https://blogbreeze-arfcaubvgqbmejg0.eastasia-01.azurewebsites.net
- **Documentation**: See `AZURE_DEPLOYMENT_STATUS.md` and `GITHUB_DEPLOYMENT_SETUP.md`

---

Made with ❤️ using Django and Azure
