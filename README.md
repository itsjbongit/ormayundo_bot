# Free Telegram Reminder Bot

# 🚀 Ormayundo

**Never forget what matters.**

Ormayundo is a Telegram-based reminder assistant designed to help users create, manage, and receive reminders effortlessly through a simple chat interface.

The goal of Ormayundo is to provide a fast, lightweight, and distraction-free reminder experience without requiring users to install another app or navigate complicated interfaces.

---

## ✨ Features

### Current Features (V1)

* 🤖 Telegram Bot Interface
* 👋 Interactive Welcome Screen
* ➕ Create New Reminders
* 📋 View Existing Reminders
* ✏️ Edit Reminder Framework
* 🗑 Delete Reminder Framework
* 💾 Persistent Storage using Firebase Firestore
* 👤 User-specific reminder management
* 🔄 Multi-step conversation flow
* 🎯 State-based interaction engine

---

## 🏗 Architecture

```text
Telegram User
      │
      ▼
Ormayundo Telegram Bot
      │
      ▼
Conversation Handlers
      │
      ▼
State Management Layer
      │
      ▼
Firebase Firestore
      │
      ▼
Reminder Engine
```

---

## 🛠 Tech Stack

### Backend

* Python 3.12+
* python-telegram-bot
* Firebase Firestore
* APScheduler (Reminder Engine)

### Infrastructure

* Telegram Bot API
* Firebase
* GitHub

### Future Infrastructure

* FastAPI
* Webhook Deployment
* Docker

## 🔐 Environment Variables

Create a `.env` file:

```env
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
GOOGLE_APPLICATION_CREDENTIALS=firebase-key.json
```

---

### Creating a Reminder

```text
User
 │
 ▼
➕ New Reminder
 │
 ▼
"What should I remind you about?"
 │
 ▼
Study DSA
 │
 ▼
"When should I remind you?"
 │
 ▼
Tomorrow 7 PM
 │
 ▼
Reminder Saved
```

---

## 🎯 Vision

Ormayundo is not intended to be just another reminder bot.

The long-term vision is to evolve into a personal productivity companion capable of helping users:

* Track tasks
* Manage schedules
* Plan study sessions
* Organize projects
* Maintain habits
* Stay productive through conversational interactions

while remaining lightweight, fast, and accessible through Telegram.

## 🤝 Contributing

Contributions, feature suggestions, and bug reports are welcome.

Feel free to fork the repository and submit a pull request.

## 👨‍💻 Author

**Jerome Biju**

Student • Developer • Builder

Passionate about creating useful software, solving real-world problems, and building products that help people stay organized and productive.

---

## 💡 Meaning Behind The Name

**Ormayundo** (ഓർമ്മയുണ്ടോ?)

A Malayalam phrase meaning:

> "Do you remember?"

The perfect name for a reminder assistant whose purpose is to make sure you never forget what matters.


There is also a landing page + admin dashboard which can be used to access the bot, and using sdmin privillage, access the statistics of BOT.


### Live at : https://ormayundo.page.gd/
