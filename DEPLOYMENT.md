# GitHub + Vercel Deployment Guide

## 🚀 Quick Deployment Steps

### 1. Initialize Git Repository
```bash
cd c:/Users/mrkir/Downloads/job
git init
git add .
git commit -m "Initial commit: Job Portal Application"
```

### 2. Create GitHub Repository
1. Go to [GitHub](https://github.com)
2. Click "New repository"
3. Name: `job-portal` (or your preferred name)
4. Choose Public/Private
5. Click "Create repository"

### 3. Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/job-portal.git
git branch -M main
git push -u origin main
```

### 4. Deploy to Vercel
1. Go to [Vercel](https://vercel.com)
2. Click "Import Project"
3. Connect your GitHub account
4. Select the `job-portal` repository
5. Click "Deploy"

## ⚙️ Vercel Configuration

### Environment Variables (Set in Vercel Dashboard):
- `SECRET_KEY`: Your Flask secret key
- `VERCEL`: Set to `true` (for production detection)

### Framework Settings:
- **Framework Preset**: Other
- **Root Directory**: `./`
- **Build Command**: Leave empty
- **Output Directory**: Leave empty

## 🔄 Auto-Deploy Setup

Once connected, Vercel will:
- ✅ Auto-deploy on every push to `main` branch
- ✅ Provide preview URLs for pull requests
- ✅ Handle SSL certificates automatically

## 📁 Project Structure for Vercel
```
job-portal/
├── app.py              # Main Flask app
├── api/
│   └── index.py        # Vercel entry point
├── templates/          # HTML templates
├── static/            # CSS/JS files
├── vercel.json        # Vercel config
├── requirements.txt    # Python dependencies
└── .gitignore        # Git ignore file
```

## 🌐 Access Your App

After deployment:
- **Production URL**: `https://your-app-name.vercel.app`
- **Preview URLs**: For each pull request
- **Dashboard**: Manage settings and view logs

## 🔧 Troubleshooting

### Common Issues:
1. **Build Errors**: Check `requirements.txt` and Python version
2. **Database Issues**: SQLite works but consider PostgreSQL for production
3. **Static Files**: Ensure they're in `/static/` folder

### Debug Mode:
- Set `VERCEL=true` in environment variables
- Check Vercel logs for errors

## 📱 Testing Your Deployment

1. Visit your Vercel URL
2. Test user registration
3. Test job posting/application
4. Verify all features work

Your Job Portal will be live and automatically updating! 🎉
