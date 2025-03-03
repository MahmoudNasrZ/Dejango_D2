# Django 

## Setup Instructions

### Prerequisites
- Python installed (`>=3.8` recommended)
- Django installed (`pip install django`)

### Installation Steps
1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd Day1
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv myenv
   source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```sh
   python manage.py migrate
   ```
5. Start the development server:
   ```sh
   python manage.py runserver
   ```
6. Open your browser and go to `http://127.0.0.1:8000/`.

## Usage
- Modify `models.py` to define database models.
- Add new views in `views.py` and link them in `urls.py`.
- Create frontend templates in `templates/`.

## Contributing
If you’d like to contribute:
- Fork the repository.
- Create a new branch (`git checkout -b feature-branch`).
- Make your changes and commit (`git commit -m "Add new feature"`).
- Push to your branch (`git push origin feature-branch`).
- Submit a pull request.
Mahmoud Nasr