import os
import django
from datetime import datetime, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ticketing_system.settings")
django.setup()

from core.models import Movie, Show  # noqa: E402


def run():
    Movie.objects.all().delete()
    Show.objects.all().delete()

    movie1 = Movie.objects.create(title="Inception", duration_minutes=148)
    movie2 = Movie.objects.create(title="Interstellar", duration_minutes=169)

    now = datetime.now()

    Show.objects.create(
        movie=movie1,
        screen_name="Screen 1",
        date_time=now + timedelta(hours=2),
        total_seats=50,
    )
    Show.objects.create(
        movie=movie1,
        screen_name="Screen 2",
        date_time=now + timedelta(hours=5),
        total_seats=40,
    )
    Show.objects.create(
        movie=movie2,
        screen_name="Screen 3",
        date_time=now + timedelta(hours=3),
        total_seats=60,
    )

    print("Seed data created.")


if __name__ == "__main__":
    run()
