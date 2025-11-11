# GitHub Actions Auto-Deployment Setup

## ✅ What I've Done:

1. Created `.github/workflows/azure-deploy.yml` - GitHub Actions workflow
2. Created `startup.sh` - Azure startup script for migrations and Gunicorn
3. Configured Azure App Service to use the startup script
4. Saved your Azure publish profile to `azure-publish-profile.xml`

## 🔐 Setup GitHub Secrets:

### Step 1: Add Azure Publish Profile

1. Go to your GitHub repo: https://github.com/YounasKhan2/BlogBreeze
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `AZURE_WEBAPP_PUBLISH_PROFILE`
5. Value: Copy the ENTIRE contents of `azure-publish-profile.xml` file
6. Click **Add secret**

### Step 2: Add Django Secret Key

1. Click **New repository secret** again
2. Name: `SECRET_KEY`
3. Value: `W3nvXMUCzLLQoyMH8S4W-_ZM7JA6A5f0ffdl7mZ9VhcqHDiC7gJtJqd9hyRlxjqjR54`
4. Click **Add secret**

## 🚀 How It Works:

Once you push code to the `main` branch:

1. GitHub Actions automatically triggers
2. Installs Python dependencies
3. Collects static files
4. Deploys to Azure App Service
5. Azure runs `startup.sh` which:
   - Runs database migrations
   - Collects static files again
   - Starts Gunicorn server

## 📝 To Deploy Now:

```bash
# Commit the new files
git add .github/workflows/azure-deploy.yml startup.sh
git commit -m "Add GitHub Actions auto-deployment"
git push origin main
```

After pushing, go to your GitHub repo → **Actions** tab to watch the deployment progress.

## 🌐 Your Live App:

Once deployed, visit: https://blogbreeze-arfcaubvgqbmejg0.eastasia-01.azurewebsites.net

## 🔧 Troubleshooting:

### View Deployment Logs:
- GitHub: Go to **Actions** tab in your repo
- Azure: `az webapp log tail --name blogbreeze --resource-group Blogbreeze`

### Manual Trigger:
You can manually trigger deployment from GitHub:
1. Go to **Actions** tab
2. Click **Deploy to Azure App Service**
3. Click **Run workflow**

### If Deployment Fails:
1. Check GitHub Actions logs for errors
2. Verify both secrets are added correctly
3. Check Azure App Service logs
4. Ensure `requirements.txt` has all dependencies

## ⚠️ Important Notes:

- **DO NOT** commit `azure-publish-profile.xml` to Git (it contains credentials)
- The file is already in `.gitignore`
- Images will now upload to Azure Blob Storage automatically
- Database migrations run automatically on each deployment

---
*Setup completed on November 11, 2025*
