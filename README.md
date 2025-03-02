# 📌 TranslatePDF (FastAPI + Vue.js)

## 🚀 Description
TranslatePDF is a service that allows users to upload, process, and translate PDF files. The backend is built with **FastAPI**, while the frontend is powered by **Vue.js**. The project uses **PostgreSQL** for data storage and is fully containerized with **Docker and Docker Compose**.

---

## 📂 Project Structure

/translatepdf
│── /app                  # 📂 Backend (FastAPI)
│   ├── /routes           # 📂 API endpoints
│   │   ├── auth.py       # 🔹 Authentication (Google OAuth, JWT)
│   │   ├── pdf.py        # 🔹 PDF file management endpoints
│   │   ├── users.py      # 🔹 User-related endpoints
│   │   ├── init.py   # 📌 Module initialization
│   ├── /models           # 📂 Database models (SQLAlchemy)
│   │   ├── user.py       # 🔹 User model
│   │   ├── pdf.py        # 🔹 PDF file model
│   │   ├── init.py   # 📌 Model initialization
│   ├── /services         # 📂 Business logic (PDF processing)
│   ├── /utils            # 📂 Utility functions (e.g., password hashing)
│   ├── config.py         # 🔹 Configuration file (paths, limits)
│   ├── database.py       # 🔹 Database connection and initialization
│   ├── dependencies.py   # 🔹 Dependency functions (e.g., get_db)
│   ├── main.py           # 🔹 FastAPI entry point
│── /frontend             # 📂 Frontend (Vue.js)
│   ├── /public           # 📂 Static assets (favicon, logo)
│   ├── /src              # 📂 Vue source code
│   │   ├── /components   # 📂 UI components (buttons, forms)
│   │   ├── /views        # 📂 Pages (LoginView.vue, DashboardView.vue)
│   │   ├── /store        # 📂 State management (Vuex/Pinia)
│   │   ├── /api          # 📂 API service (Axios)
│   │   ├── App.vue       # 🔹 Main Vue component
│   │   ├── main.js       # 🔹 Vue entry point
│   ├── index.html        # 🔹 Main HTML file
│   ├── vite.config.js    # 🔹 Vite configuration
│   ├── package.json      # 🔹 Frontend dependencies
│── /docker               # 📂 Docker configuration
│   ├── backend.Dockerfile # 🔹 Dockerfile for FastAPI backend
│   ├── frontend.Dockerfile # 🔹 Dockerfile for Vue.js frontend
│   ├── nginx.conf        # 🔹 Nginx configuration
│── /data                 # 📂 Directory for uploaded PDF files
│── /logs                 # 📂 Server logs (backend + frontend)
│── .env.example          # 🔹 Environment variable template
│── .env                  # 🔹 Environment variables (ignored in Git)
│── docker-compose.yml    # 🔹 Docker Compose configuration
│── requirements.txt      # 🔹 Python dependencies
│── README.md             # 🔹 Project documentation

---

## **⚡ Quick Start**
### **1️⃣ Clone the repository**
```bash
git clone https://github.com/your-repo/translatepdf.git
cd translatepdf

2️⃣ Set up environment variables

cp .env.example .env

Fill in the necessary values, such as DATABASE_URL and Google OAuth credentials.

3️⃣ Start the application

docker-compose up --build -d

The application should now be running!

🔗 API Documentation (Swagger)

Once the backend is running, you can access the API documentation at:
👉 http://localhost:8000/docs

🎨 Frontend Development
	•	Frontend codebase: Located in /frontend/
	•	Run frontend in Docker:

docker-compose up frontend


	•	API Base URL: http://localhost:8000

🛠️ Tech Stack
	•	Backend: FastAPI, SQLAlchemy, PostgreSQL, Uvicorn
	•	Frontend: Vue.js (Vite), Axios
	•	Authentication: Google OAuth, JWT (JSON Web Token)
	•	Infrastructure: Docker, Docker Compose, Nginx

✅ Features
	•	✅ User authentication via Google OAuth
	•	✅ Secure JWT-based session management
	•	✅ Upload and manage PDF files
	•	✅ Delete and list uploaded PDF files
	•	✅ Frontend integration with Vue.js
	•	✅ Fully containerized using Docker

🚀 Contribution Guide
	1.	Fork the repository.
	2.	Create a new branch for your feature.
	3.	Commit your changes and push them.
	4.	Open a Pull Request (PR) for review.

📜 License

This project is licensed under the MIT License.

🚀 Happy Coding! 🎉
For any issues or suggestions, feel free to create an issue on GitHub!