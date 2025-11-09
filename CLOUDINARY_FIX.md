# Cloudinary Image Upload Fix

## Problem
Images were not uploading to Cloudinary in production, causing 404 errors for post images.

## Root Causes Fixed

### 1. App Order Issue
**Problem:** `cloudinary_storage` was listed AFTER `django.contrib.staticfiles` in `INSTALLED_APPS`.
**Fix:** Moved `cloudinary_storage` BEFORE `staticfiles` - this is required for Cloudinary to properly intercept file uploads.

### 2. CKEditor Storage Backend
**Problem:** CKEditor wasn't explicitly configured to use Cloudinary storage in production.
**Fix:** Added `CKEDITOR_STORAGE_BACKEND = 'cloudinary_storage.storage.MediaCloudinaryStorage'` for production.

### 3. Settings Configuration
**Problem:** Media storage settings weren't properly separated between dev and production.
**Fix:** Updated settings to use local storage in DEBUG mode and Cloudinary in production.

## Deployment Steps

### 1. Verify Cloudinary Credentials in Render
Go to your Render dashboard → Your service → Environment and ensure these are set:

```
CLOUDINARY_CLOUD_NAME=your_cloud_name_here
CLOUDINARY_API_KEY=your_api_key_here
CLOUDINARY_API_SECRET=your_api_secret_here
DEBUG=False
```

### 2. Deploy the Changes
```bash
git add .
git commit -m "Fix Cloudinary image upload configuration"
git push origin main
```

Render will automatically redeploy.

### 3. Test Image Upload
1. Go to your production site admin panel
2. Create a new blog post
3. Upload a featured image
4. Save and publish the post
5. View the post - image should display correctly
6. Check your Cloudinary dashboard - the image should appear there

## How It Works Now

### Development (DEBUG=True)
- Images save to local `media/` folder
- Served by Django development server
- No Cloudinary needed

### Production (DEBUG=False)
- Images upload directly to Cloudinary
- Cloudinary serves the images via CDN
- Images persist across deployments
- Both featured images and CKEditor uploads use Cloudinary

## Troubleshooting

### Images still showing 404 in production?
1. Check Render environment variables are set correctly
2. Check Render logs for Cloudinary connection errors
3. Verify `DEBUG=False` in production
4. Try uploading a NEW image (old images uploaded before the fix won't be in Cloudinary)

### Images work in admin but not on frontend?
- Check your templates are using `{{ post.featured_image.url }}` correctly
- Verify the image field is not empty in the database

### CKEditor images not uploading?
- Check browser console for errors
- Verify `ckeditor_uploader` is in INSTALLED_APPS
- Check that `/ckeditor/` URL is in your main urls.py
