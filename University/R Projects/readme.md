# 🌟 Interactive R in Colab Playground

![Google Colab](https://img.shields.io/badge/Google%20Colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white&color=F9AB00)

![R Language](https://img.shields.io/badge/R-276DC3?style=for-the-badge&logo=r&logoColor=white)

**One-click R scripting in Google Colab - No setup required!**



## 🎯 Quick Start Guide

### 🚀 3-Step Setup

```
1. 📱 **Create** → New notebook in Google Colab
2. ⚙️  **Switch** → Runtime → Change runtime type → Select "R"
3. 🎮 **Paste** → Your R code into the cell → Run!
```

### 🎨 Visual Walkthrough

Step Action Visual
1 Click "New notebook" in Colab [+] New notebook
2 Navigate to Runtime → Change runtime type Runtime → Change runtime type
3 Select "R" from dropdown Python → R ✅
4 Paste & Run your code! [Ctrl] + [Enter]

### 💡 Example Magic

```r
# 🎯 Paste this in your first Colab R cell!
print("🎉 Welcome to R in Colab!")

# 📊 Quick visualization demo
library(ggplot2)
data <- data.frame(
  category = c('A', 'B', 'C', 'D'),
  values = c(23, 45, 56, 12)
)

ggplot(data, aes(x=category, y=values, fill=category)) +
  geom_bar(stat='identity') +
  theme_minimal() +
  labs(title='🎨 Your First R Plot in Colab!')
```

### 🛠️ Features & Benefits

✅ What You Get

Feature Benefit
⚡ Zero Setup No installation needed
🆓 Free Tier Google's free compute resources
📦 Pre-installed Packages Most popular R libraries ready
💾 Cloud Storage Save directly to Google Drive
🤝 Easy Sharing Share notebooks with one click

🎪 Interactive Elements

<details>
<summary>🔄 <b>Click to expand: Runtime Switching Guide</b></summary>

<br>

Visual Path:

```
File → New notebook → Runtime menu → Change runtime type → R → Save
```

Pro Tip: You can also use GPU/TPU acceleration for faster computations!

</details>

<details>
<summary>📚 <b>Click to expand: Sample Code Library</b></summary>

<br>

```r
# 🔥 Data Analysis Sample
library(dplyr)
library(ggplot2)

# Sample data manipulation
starwars %>%
  filter(species == "Human") %>%
  ggplot(aes(x = height, y = mass)) +
  geom_point(aes(color = gender)) +
  labs(title = "Star Wars Humans: Height vs Mass")
```

</details>

### 🚀 Advanced Usage

📋 **Keyboard Shortcuts Cheatsheet**

Action Shortcut
Run cell Ctrl + Enter
Run & advance Shift + Enter
Insert cell above Ctrl + M A
Insert cell below Ctrl + M B

## 🎯 Pro Tips

```r
# Install additional packages if needed
install.packages("your_package")
library(your_package)

# Access files from Google Drive
library(googledrive)
# ... your file operations here
```

## 🆘 Troubleshooting

<details>
<summary>❌ <b>Common Issues & Solutions</b></summary>

<br>

Issue: "Runtime not found"

· ✅ Solution: Make sure you're signed into Google account

Issue: Packages not loading

· ✅ Solution: Use install.packages() first

Issue: Plot not showing

· ✅ Solution: Ensure library(ggplot2) is loaded

</details>

## 🎊 Ready to Explore?

<div align="center">

Your R adventure starts now!

https://colab.research.google.com/assets/colab-badge.svg

⭐ Star this repo if you found it helpful!

---

Made with ❤️ for the R community | Happy coding! 🎉

</div>