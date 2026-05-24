# Deployment Guide for Render

This guide will help you deploy the Todos API to Render.

## Prerequisites

- A Render account (free tier available)
- Git repository with your code
- PostgreSQL database credentials

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
2. Click **New +** and select **Blueprint**
3. Connect your Git repository
4. Render will automatically detect the `render.yaml` file and configure the service
5. Click **Deploy Blueprint**

### 3. Database Setup

The `render.yaml` file will automatically create a PostgreSQL database named `todos-db` on Render's free tier.

> **Note:** MySQL is not available on Render's free tier. Use PostgreSQL (already configured).

### 4. Environment Variables

The following environment variables are automatically configured by `render.yaml`:

- `DB_CONNECTION`: Set to `postgresql`
- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_DATABASE`: Auto-populated from the database
- `SECRET_KEY`: Auto-generated secure key
- `FRONTEND_URL`: Update this to your frontend URL when ready

The following must be added **manually** in the Render dashboard (Environment tab) after deploying:

- `JWT_SECRET_KEY`: Your JWT secret key
- `JWT_ALGORITHM`: e.g. `HS256`
- `JWT_EXPIRATION_TIME`: e.g. `3600`
- `CLOUDINARY_CLOUD_NAME`: Your Cloudinary cloud name
- `CLOUDINARY_API_KEY`: Your Cloudinary API key
- `CLOUDINARY_API_SECRET`: Your Cloudinary API secret

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
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_TIME=3600
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
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
- Visit your API URL (e.g., `https://todos-api.onrender.com/home`)
- You should see: `{"status":"success","message":"What's everyone working on today?"}`

## Important Notes

### Database Choice
- **PostgreSQL**: Available on Render's free tier (recommended and configured)
- **MySQL**: Not available on free tier, requires a paid plan

### CORS Configuration
Update the `FRONTEND_URL` environment variable to match your frontend domain to allow CORS requests. You can use `http://localhost:3000` as a placeholder during development and update it later from the Render dashboard.

### Static Files
The application serves static files from the `/static` endpoint. Ensure your static files are in the `app/static` directory. Note that Render's filesystem is ephemeral — use Cloudinary for persistent file/image storage.

### Cloudinary
Add the following environment variables in the Render dashboard for image uploads to work:
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
- Ensure all dependencies are in `requirements.txt` (especially `psycopg2-binary`)

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
uvicorn main:app --reload
```