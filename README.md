# Dynamic Web Portfolio - CS50 Final Project

#### **Video Demo:** [https://youtu.be/VClqyen1j3Y?si=rqiCpyMeu5eWw64s](https://youtu.be/VClqyen1j3Y?si=rqiCpyMeu5eWw64s)

---

## Description
This project is a **Full-Stack Dynamic Web Portfolio** built with **Python, Flask, and SQLite3**. It serves as a professional digital resume where I can showcase my skills, projects, and educational background. 

The core innovation is its custom **Content Management System (CMS)**. Unlike static portfolios, this site includes a secure administrative dashboard that allows me to update my professional profile in real-time without modifying the source code.

---

## Tech Stack

| Component | Technology |
| :--- | :--- |
| **Backend** | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) |
| **Database** | ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) |
| **Frontend** | ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white) ![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white) |
| **Interactivity** | ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) |
---

## Key Features
- **Dynamic Data Rendering:** Every section (projects, skills, professional timeline) is populated seamlessly from the `portfolio.db` database.
- **Secure Admin Panel:** Protected by user authentication, session management, and password hashing (`werkzeug.security`) to ensure data safety.
- **Full CRUD Functionality:**
  - **Create:** Add new projects, technical skills, and educational timeline events.
  - **Read:** Display all information dynamically on the frontend.
  - **Update:** Edit existing project details, skill percentages, or experiences.
  - **Delete:** Remove outdated records or manage incoming messages.
- **Dynamic CV Management:** A dedicated feature within the dashboard that allows the admin to upload and update the downloadable resume (PDF) directly to the server.
- **Interactive & Responsive UI:** A fully mobile-friendly "hacker" dark theme built with Bootstrap 5, enhanced with custom CSS and JavaScript for scroll-reveal animations.
- **Contact System:** A functional form that stores visitor inquiries securely in the database for the administrator to review from the dashboard.
- **Custom Error Handling:** A personalized, themed 404 error page that gracefully handles invalid routes and guides users back to the main site.

---

## File Structure and Components

The project is modularly organized to ensure scalability and maintainability:

- `app.py`: The main application controller. It configures Flask, handles routing, database connections, and session security using custom decorators.
- `portfolio.db`: The SQLite3 relational database containing all dynamic data (`proyectos`, `habilidades`, `trayectoria`, `mensajes`,`usuarios `).
- `requirements.txt`: Lists all Python dependencies required to run the application.
- `static/`: Directory containing custom CSS (neon effects), JavaScript (scroll animations), user-uploaded images, and the downloadable CV.
- `templates/`: Directory containing all Jinja2 HTML templates (`layout.html`, `index.html`, `admin.html`, edit forms, and the custom `404.html`).


### Frontend Views (Templates)
| File | Purpose |
| :--- | :--- |
| `layout.html` | Base template with the navbar, footer, and global styles. |
| `index.html` | The landing page. Dynamically displays skills and the project gallery. |
| `admin.html` | The dashboard for managing site content and reading messages. |
| `login.html` / `register.html` | Authentication views for administrator access. |
| `edit.html` / `edit_skill.html` / `edit_trayectoria.html` | Specific forms for updating database entries. |
| `enviar_mensaje.html` | The public contact form interface. |
| `404.html` | Custom error page with a themed "segmentation fault" message. |

---

## Design Decisions

1. **Backend Logic & Framework:** I selected **Python** with Flask as the core of this project. Python is my primary programming language, deeply rooted in my technical high school curriculum. This solid foundation allowed me to focus on building a robust, secure Content Management System rather than struggling with backend syntax.
2. **Frontend & Aesthetics:** I implemented a "Dark Hacker" theme using CSS variables and **Bootstrap 5** to create a high-contrast, professional environment. I chose Bootstrap alongside HTML, CSS, and JavaScript not only because they were covered in CS50, but also because I have extensive prior experience with them through my technical high school education and my Junior Achievement certification.
3. **Database Architecture:** I chose **SQLite3** for its portability and seamless integration with Python. This decision was driven both by its use in the CS50 curriculum and my prior solid background in relational databases (having previously worked with Oracle DB). It perfectly supports the relational structure needed between projects, skills, and messages.
4. **User Experience (UX):** To differentiate this from a basic static page, I utilized vanilla JavaScript to create "Scroll Reveal" micro-interactions. This ensures that navigating through the professional timeline and project gallery feels fluid, modern, and engaging.

> [!IMPORTANT]
> **Reflections on CS50:**
> "I believe it is crucial that this course remains free, as it allows people from all over the world to grow in the beautiful field of programming. Personally, it has helped me immensely to develop both mentally and professionally. Thank you for all your help and dedication!"

---

## Screenshots (Placeholders)

|                      Home View                          |                            Admin Dashboard                             |
| :-----------------------------------------------------: | :--------------------------------------------------------------------: |
| ![Home Screenshot](/static/screenshots/home/Home.jpg)   | ![Admin Screenshot](/static/screenshots/admin/Admin%20CV.jpg)          |
| ![Home Skills](/static/screenshots/home/Skills.jpg)     | ![Admin Skills](/static/screenshots/admin/Admin%20Proyects-Skills.jpg) |
| ![Home Proyects](/static/screenshots/home/Proyects.jpg) | ![Admin Edit Proyects](/static/screenshots/admin/Edit%20Proyects.jpg)  |

## Installation & Usage

To run this project locally, follow these steps:

1. **Clone the repository:**
   ```bash
    git clone https://github.com/Arielpirata07/portafolio-cs50
    ```

2. **Navigate to the project directory:**
    ```bash
    cd final_proyect
    ```

3. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Run the Flask application:**
    ```bash
    flask run
    ```
5. **Access the site:** 
Open your web browser and go to http://127.0.0.1:5000. To access the admin panel, navigate to /login (Default credentials can be configured in the database).
