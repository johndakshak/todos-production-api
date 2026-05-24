# Deployment Guide for Render

This guide will help you deploy the Farm Connect API to Render.

## Prerequisites

- A Render account (free tier available)
- Git repository with your code
- PostgreSQL or MySQL database credentials

## Deployment Steps

### 1. Push Code to Git Repository

Ensure your code is pushed to a Git repository (GitHub, GitLab, or Bitbucket).

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Create a New Web Service on Render

1. Log in to [Render](https://render.com)
2. Click **New +** and select **Web Service**
3. Connect your Git repository
4. Render will automatically detect the `render.yaml` file and configure the service
5. Click **Create Web Service**

### 3. Database Setup

The `render.yaml` file will automatically create a PostgreSQL database named `farm-connect-db` on Render's free tier.

If you prefer to use MySQL instead:
- Change `DB_CONNECTION` to `mysql` in render.yaml
- Note: MySQL is not available on Render's free tier

### 4. Environment Variables

The following environment variables are automatically configured by render.yaml:

- `DB_CONNECTION`: Set to `postgresql` (or `mysql` if using MySQL)
- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_DATABASE`: Auto-populated from database
- `SECRET_KEY`: Auto-generated secure key
- `FRONTEND_URL`: Update this to your frontend URL

### 5. Manual Environment Variables (if not using render.yaml)

If you're not using the `render.yaml` file, manually add these environment variables in Render:

```
DB_CONNECTION=postgresql
DB_HOST=your-database-host
DB_PORT=5432
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_DATABASE=todos
SECRET_KEY=your-secret-key-here
FRONTEND_URL=https://your-frontend-url.com
```

### 6. Run Database Migrations

After deployment, you'll need to run Alembic migrations to create the database tables:

1. Go to your web service in Render
2. Click **Shell** to open a web shell
3. Run the following commands:

```bash
cd app
alembic upgrade head
```

### 7. Verify Deployment

Once the deployment is complete:
- Check the deployment logs for any errors
- Visit your API URL (e.g., `https://farm-connect-api.onrender.com/home`)
- You should see: `{"status":"success","message":"What's everyone working on today?"}`

## Important Notes

### Database Choice
- **PostgreSQL**: Available on Render's free tier (recommended)
- **MySQL**: Not available on free tier, requires paid plan

### CORS Configuration
Update the `FRONTEND_URL` environment variable to match your frontend domain to allow CORS requests.

### Static Files
The application serves static files from `/static` endpoint. Ensure your static files are in the `app/static` directory.

### Cloudinary
If you're using Cloudinary for image uploads, ensure you add the following environment variables:
- `CLOUDINARY_CLOUD_NAME`
- `CLOUDINARY_API_KEY`
- `CLOUDINARY_API_SECRET`

## Troubleshooting

### Database Connection Errors
- Verify database credentials in environment variables
- Ensure the database is running and accessible
- Check the database logs in Render

### Migration Issues
- Ensure Alembic is properly configured
- Check that the database connection string is correct
- Run `alembic current` to check migration status

### Application Not Starting
- Check the deployment logs in Render
- Verify the Dockerfile is correct
- Ensure all dependencies are in requirements.txt

## Local Development with PostgreSQL

To test locally with PostgreSQL before deploying:

1. Install PostgreSQL locally
2. Update your `.env` file:
```
DB_CONNECTION=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your-password
DB_DATABASE=todos
```

3. Run migrations:
```bash
cd app
alembic upgrade head
```

4. Start the application:
```bash
uvicorn app.main:app --reload
```
