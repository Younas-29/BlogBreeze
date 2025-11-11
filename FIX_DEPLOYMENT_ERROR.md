# Fix Deployment Error - Missing GitHub Secrets

## ❌ Error
```
Error: Deployment failed, Error: No credentials found
```

## 🔧 Solution

You need to add the Azure publish profile as a GitHub secret.

### Step 1: Get the Publish Profile

The publish profile is already saved in your local file: `azure-publish-profile.xml`

### Step 2: Add GitHub Secret

1. Go to your GitHub repository: **https://github.com/Younas-29/BlogBreeze**

2. Click **Settings** (top menu)

3. In the left sidebar, click **Secrets and variables** → **Actions**

4. Click the green **New repository secret** button

5. Add the first secret:
   - **Name**: `AZURE_WEBAPP_PUBLISH_PROFILE`
   - **Value**: Open the file `azure-publish-profile.xml` and copy **ALL** its content (the entire XML)
   - Click **Add secret**

6. Add the second secret:
   - Click **New repository secret** again
   - **Name**: `SECRET_KEY`
   - **Value**: `W3nvXMUCzLLQoyMH8S4W-_ZM7JA6A5f0ffdl7mZ9VhcqHDiC7gJtJqd9hyRlxjqjR54`
   - Click **Add secret**

### Step 3: Re-run the Deployment

After adding the secrets:

**Option A: Push a new commit**
```bash
git commit --allow-empty -m "Trigger deployment after adding secrets"
git push origin azd-enable-copilot-coding-agent-with-azure
```

**Option B: Re-run from GitHub**
1. Go to: https://github.com/Younas-29/BlogBreeze/actions
2. Click on the failed workflow run
3. Click **Re-run all jobs**

### ✅ Verify Secrets Are Added

Go to: https://github.com/Younas-29/BlogBreeze/settings/secrets/actions

You should see:
- ✅ `AZURE_WEBAPP_PUBLISH_PROFILE`
- ✅ `SECRET_KEY`

---

**Important**: The `azure-publish-profile.xml` file contains sensitive credentials. Make sure it's in `.gitignore` and never commit it to Git!
