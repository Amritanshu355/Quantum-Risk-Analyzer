# 🚀 Deployment Guide - Streamlit Cloud

This guide walks you through deploying the Quantum Risk Analyzer to Streamlit Cloud.

---

## 📋 Prerequisites

1. **GitHub Account** - You need a GitHub account to host your repository
2. **Streamlit Cloud Account** - Free at [share.streamlit.io](https://share.streamlit.io)

---

## Step 1: Prepare Your Repository

### Initialize Git (if not already done)

```bash
cd quantum-risk-analyzer
git init
git add .
git commit -m "Initial commit: Quantum Risk Analyzer v2.0"
```

### Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `quantum-risk-analyzer`
3. Choose Public (recommended) or Private
4. Click **"Create repository"**

### Push to GitHub

```bash
# Replace with your GitHub username
git remote add originhttps://github.com/Amritanshu355/Quantum-Risk-Analyzer/tree/main/Quantum-Risk-Analyzer
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy to Streamlit Cloud

### Access Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account

### Create New App

1. Click **"New App"** button
2. Fill in the deployment form:

| Field | Value |
|-------|-------|
| **App Type** | Single Page App |
| **Repository** | `yourusername/quantum-risk-analyzer` |
| **Branch** | `main` |
| **Main File Path** | `app.py` |

3. Click **"Advanced Settings"** (optional):
   - Set environment variables if needed
   - Configure secrets if using API keys

4. Click **"Deploy!"**

---

## Step 3: Monitor Deployment

1. Streamlit Cloud will show deployment logs
2. Initial deployment takes ~2-5 minutes
3. Once complete, you'll see:
   - ✅ **"Deployment successful!"**
   - A live URL like: `https://yourapp-share.streamlit.app`

---

## Step 4: Configure Custom Domain (Optional)

1. In Streamlit Cloud dashboard, select your app
2. Click **"Settings"** → **"Custom Domain"**
3. Follow DNS configuration instructions
4. Wait for DNS propagation (up to 24 hours)

---

## 🔧 Troubleshooting

### Deployment Fails with "Module Not Found"

**Solution:** Ensure `requirements.txt` is in the repository root:

```bash
# Verify file exists
ls requirements.txt

# If missing, create it
echo "streamlit>=1.53.1
pandas>=2.3.3
numpy>=2.4.1
plotly>=6.5.2" > requirements.txt

git add requirements.txt
git commit -m "Add requirements.txt"
git push
```

### App Loads but Shows Errors

**Check the following:**

1. **Python Version**: Streamlit Cloud uses Python 3.11+ by default
2. **File Paths**: Ensure all imports use relative paths
3. **Memory Limits**: Free tier has ~1GB RAM limit

### View Deployment Logs

1. Go to your app in Streamlit Cloud
2. Click **"Manage App"** → **"Logs"**
3. Review error messages

---

## 📊 Performance Tips

### Optimize for Streamlit Cloud

1. **Use Caching**: The app already uses `@st.cache_data` where appropriate
2. **Limit Data Size**: Sample data is ~10 assets; keep under 100 for best performance
3. **Optimize Plots**: Plotly charts are already optimized for web

### Expected Performance

| Metric | Target |
|--------|--------|
| Initial Load | < 5 seconds |
| Tab Switching | < 2 seconds |
| Chart Rendering | < 3 seconds |

---

## 🔐 Security Best Practices

### Using Secrets

For production deployments with sensitive data:

1. Create `.streamlit/secrets.toml` locally (never commit!)
2. Add secrets in Streamlit Cloud dashboard:
   - Settings → Secrets → Add Secret

Example `secrets.toml`:
```toml
[api_keys]
some_api_key = "your-actual-key"
```

Access in code:
```python
import streamlit as st
api_key = st.secrets["api_keys"]["some_api_key"]
```

---

## 💰 Pricing

Streamlit Cloud offers:

| Plan | Price | Best For |
|------|-------|----------|
| **Free** | $0 | Personal projects, demos |
| **Pro** | $29/month | Production apps, custom domains |
| **Team** | Custom | Enterprise deployments |

For a resume project, the **Free tier** is sufficient!

---

## 📈 Post-Deployment Checklist

- [ ] App loads without errors
- [ ] All tabs are functional
- [ ] Charts render correctly
- [ ] Download buttons work
- [ ] Sidebar configuration updates results
- [ ] Share URL works for others

---

## 🎉 Success!

Your Quantum Risk Analyzer is now live! Share your deployment:

- Add the URL to your resume
- Include in your portfolio
- Share on LinkedIn

Example resume bullet:
> **Quantum Risk Analyzer** - Deployed at [yourapp.share.streamlit.app](https://yourapp.share.streamlit.app)
> - Built enterprise-grade risk assessment platform using Streamlit, Python, and Plotly
> - Implemented AI-powered recommendation engine for cryptographic migration planning

---

## 🆘 Need Help?

- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)
- **Community Forum**: [discuss.streamlit.io](https://discuss.streamlit.io)
- **GitHub Issues**: Report bugs in this repository

---

*Happy Deploying! 🚀*
