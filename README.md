# 🎬 Movie Ticket Booking System

A robust REST API for booking movie tickets built with Django, Django REST Framework, and JWT authentication. This system handles movie listings, show scheduling, seat bookings with concurrency control, and user authentication.

## 🚀 Features

- **JWT Authentication** - Secure user signup and login with token-based authentication
- **Movie Management** - Browse available movies and their details
- **Show Listings** - View all shows for a specific movie
- **Seat Booking** - Book specific seats with real-time availability checking
- **Booking Management** - View and cancel your bookings
- **Concurrency Control** - Prevents double booking and overbooking using database transactions
- **API Documentation** - Interactive Swagger/OpenAPI documentation

## 📋 Requirements

- Python 3.8+
- Django 5.0+
- Django REST Framework
- djangorestframework-simplejwt
- drf-yasg

## 🛠 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Madhukola8/ticketing_system.git
cd ticketing_system
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 6. Load Sample Data

```bash
python seed_script.py
```

This creates sample movies (Inception, Interstellar) and shows.

### 7. Run the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## 📚 API Documentation

Interactive Swagger documentation is available at:

```
http://127.0.0.1:8000/swagger/
```

## 🔑 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/signup` | Register a new user | No |
| POST | `/login` | Login and get JWT tokens | No |

### Movies & Shows

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/movies/` | List all movies | No |
| GET | `/movies/<id>/shows/` | List all shows for a movie | No |

### Bookings

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/shows/<id>/book/` | Book a seat | Yes |
| POST | `/bookings/<id>/cancel/` | Cancel a booking | Yes |
| GET | `/my-bookings/` | List your bookings | Yes |

## 🎯 API Usage Examples

### 1. Register a User

```bash
curl -X POST http://127.0.0.1:8000/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com"
}
```

### 2. Login

```bash
curl -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepass123"
  }'
```

**Response:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 3. List Movies

```bash
curl -X GET http://127.0.0.1:8000/movies/
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Inception",
    "duration_minutes": 148
  },
  {
    "id": 2,
    "title": "Interstellar",
    "duration_minutes": 169
  }
]
```

### 4. List Shows for a Movie

```bash
curl -X GET http://127.0.0.1:8000/movies/1/shows/
```

**Response:**
```json
[
  {
    "id": 1,
    "movie": {
      "id": 1,
      "title": "Inception",
      "duration_minutes": 148
    },
    "screen_name": "Screen 1",
    "date_time": "2025-11-25T19:23:03.327353Z",
    "total_seats": 50
  }
]
```

### 5. Book a Seat

```bash
curl -X POST http://127.0.0.1:8000/shows/1/book/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "seat_number": 15
  }'
```

**Response:**
```json
{
  "id": 1,
  "show": {
    "id": 1,
    "movie": {
      "id": 1,
      "title": "Inception",
      "duration_minutes": 148
    },
    "screen_name": "Screen 1",
    "date_time": "2025-11-25T19:23:03.327353Z",
    "total_seats": 50
  },
  "seat_number": 15,
  "status": "booked",
  "created_at": "2025-11-25T16:30:00Z"
}
```

### 6. View My Bookings

```bash
curl -X GET http://127.0.0.1:8000/my-bookings/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 7. Cancel a Booking

```bash
curl -X POST http://127.0.0.1:8000/bookings/1/cancel/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "detail": "Booking cancelled successfully."
}
```

## 🔐 Authentication

This API uses JWT (JSON Web Token) authentication. After logging in, you'll receive two tokens:

- **Access Token** - Short-lived (60 minutes), used for API requests
- **Refresh Token** - Long-lived (1 day), used to get new access tokens

### Using JWT Tokens

Include the access token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

### In Swagger UI

1. Click the **Authorize** button (🔓)
2. Enter: `Bearer <your_access_token>`
3. Click **Authorize**
4. Now you can test authenticated endpoints

## 🛡️ Business Rules Implemented

1. **Double Booking Prevention** - A seat cannot be booked twice for the same show
2. **Overbooking Prevention** - Total bookings cannot exceed show capacity
3. **Seat Validation** - Seat numbers must be within valid range (1 to total_seats)
4. **Authorization** - Users can only cancel their own bookings
5. **Status Management** - Cannot cancel already cancelled bookings
6. **Concurrency Handling** - Database-level locking prevents race conditions

## 🏗️ Project Structure

```
ticketing_system/
├── core/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py          # Admin panel configuration
│   ├── models.py         # Movie, Show, Booking models
│   ├── serializers.py    # DRF serializers
│   ├── views.py          # API views/endpoints
│   └── urls.py           # URL routing
├── ticketing_system/
│   ├── __init__.py
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py
├── manage.py
├── requirements.txt
├── seed_script.py        # Sample data loader
└── README.md
```

## 🗄️ Database Models

### Movie
- `title` - Movie name
- `duration_minutes` - Movie duration

### Show
- `movie` - Foreign key to Movie
- `screen_name` - Theater screen identifier
- `date_time` - Show date and time
- `total_seats` - Total available seats

### Booking
- `user` - Foreign key to User
- `show` - Foreign key to Show
- `seat_number` - Booked seat number
- `status` - 'booked' or 'cancelled'
- `created_at` - Booking timestamp

**Unique Constraint:** `(show, seat_number, status)` - Prevents duplicate active bookings

## 🔧 Configuration

### JWT Token Lifetimes

Edit `ticketing_system/settings.py`:

```python
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}
```

### Database

By default, the project uses SQLite. To use PostgreSQL or MySQL, update the `DATABASES` setting in `settings.py`.

## 🧪 Testing

Run tests (if implemented):

```bash
python manage.py test
```

## 📝 Future Enhancements

- [ ] Add unit tests for booking logic
- [ ] Implement seat selection UI
- [ ] Add payment gateway integration
- [ ] Email notifications for bookings
- [ ] Advanced search and filtering
- [ ] Booking history and analytics
- [ ] Multi-language support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Madhu Kola**
- GitHub: [@Madhukola8](https://github.com/Madhukola8)

## 🙏 Acknowledgments

- Django Documentation
- Django REST Framework
- djangorestframework-simplejwt
- drf-yasg for API documentation

---

**Note:** This is a backend assignment project. For production use, ensure proper security measures, environment variables, and production-grade database configuration.
