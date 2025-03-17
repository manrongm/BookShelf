# BookShelf (Web Application)

Our web application empowers users to efficiently manage and track their book collections and reading plans through an intuitive and personalized platform, enhancing their reading experience.

## Product Vision Statement

"Our web application empowers users to efficiently manage and track their book collections and reading plans through an intuitive and personalized platform, enhancing their reading experience."

## How Our Project Works

Our platform offers an all-in-one solution for book lovers to organize and track their reading habits. Users can create personal book collections, set reading goals, and monitor their progress in an interactive and seamless manner. The application provides key features such as adding and editing book details, deleting unwanted books and plans, and filtering collections through a keyword-based search. 

The system is built with Flask and MongoDB, ensuring a smooth user experience with secure authentication. Users can log in to their accounts to access their customized reading data, manage their collections, and update their reading plans. The dashboard presents an intuitive layout where users can navigate through their book lists, view summaries, and track progress toward their reading goals. 

Key functionalities include:
- Secure user authentication to access personal book collections.
- Ability to add, edit, and remove books with relevant details (title, author, rating, reviews, etc.).
- Setting up and tracking personalized reading plans.
- Viewing book details and notes in an easy-to-navigate dashboard.
- Searching for books within the collection using keywords.
- Monitoring progress toward reading goals with visual indicators.

## User Stories

- As a user, I want to delete the book and reading plan I don't want anymore so that I can update my book collection and reading plans as the way I want.
- As a user, I want to be able to login to look at my own book data, so that my book collection remains clear.
- As a user, I want to be able to track my progress for my reading plan accordingly.
- As a user, I want to be able to set up a reading plan so that I can encourage myself to read.
- As a user, I want to see detailed information about each book so that I can read the notes and reviews I’ve written for it.
- As a user, I want to view a list of all the books I’ve added so that I can easily track what I’ve read or plan to read.
- As a user, I want a clean and simple dashboard so that I can easily navigate through my book collection.
- As a user, I want to search for books by some keywords so that I can quickly find a specific book in my collection.
- As a user, I want to edit book details such as title, author, rating, or review so that my book collection remains up to date.
- As a user, I want to add new books with titles, authors, genres, and ratings so that I can track my reading progress.

Also available in the [issues page](https://github.com/software-students-spring2025/2-web-app-membersonly/issues)

## Steps Necessary to Run the Software

1. **Clone the repository**
   ```bash
   git clone https://github.com/software-students-spring2025/2-web-app-membersonly.git
   cd 2-web-app-membersonly
   ```
2. **Install dependencies**
   ```bash
   pip install flask flask-wtf flask-login flask-bcrypt pymongo python-dotenv
   ```
3. **Set up .env file**
    ```bash
    SECRET_KEY= 000
    MONGO=mongodb+srv://FlaskProject2:FlaskProjectPass@bookreview.08j3l.mongodb.net/?retryWrites=true&w=majority&appName=BookReview
    ```
4. **Start the Flask application**
   ```bash
   python app.py
   ```
5. **Access the application**
   Open your web browser and navigate to: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Task Boards

Stay updated on our progress through our task boards and issue tracking:

- [Issues Page](https://github.com/software-students-spring2025/2-web-app-membersonly/issues)
- **Sprint 1:** [Sprint 1 Task Board](https://github.com/orgs/software-students-spring2025/projects/54/views/2)
- **Sprint 2:** [Sprint 2 Task Board](https://github.com/orgs/software-students-spring2025/projects/54/views/3)

These boards help us track development progress, feature implementation, and bug fixes while ensuring we meet our goals efficiently.