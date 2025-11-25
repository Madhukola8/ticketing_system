from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Movie, Show, Booking
from .serializers import (
    UserSignupSerializer,
    MovieSerializer,
    ShowSerializer,
    BookingSerializer,
    BookingCreateSerializer,
)


# ---------- Auth ----------

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(TokenObtainPairView):
    """
    Returns access and refresh JWT tokens.
    """
    permission_classes = [permissions.AllowAny]


# ---------- Movies & Shows ----------

class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]


class MovieShowsListView(generics.ListAPIView):
    serializer_class = ShowSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        movie_id = self.kwargs["movie_id"]
        return Show.objects.filter(movie_id=movie_id)


# ---------- Bookings ----------

class BookSeatView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        security=[{'Bearer': []}],
        request_body=BookingCreateSerializer,
        responses={201: BookingSerializer}
    )
    def post(self, request, show_id):
        show = get_object_or_404(Show, id=show_id)
        serializer = BookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        seat_number = serializer.validated_data["seat_number"]

        if seat_number > show.total_seats:
            return Response(
                {"detail": "Seat number exceeds total seats."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            with transaction.atomic():
                if Booking.objects.select_for_update().filter(
                    show=show,
                    seat_number=seat_number,
                    status=Booking.STATUS_BOOKED,
                ).exists():
                    return Response(
                        {"detail": "This seat is already booked."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                active_bookings = Booking.objects.select_for_update().filter(
                    show=show,
                    status=Booking.STATUS_BOOKED,
                ).count()
                if active_bookings >= show.total_seats:
                    return Response(
                        {"detail": "Show is fully booked."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                booking = Booking.objects.create(
                    user=request.user,
                    show=show,
                    seat_number=seat_number,
                    status=Booking.STATUS_BOOKED,
                )
        except Exception as e:
            return Response(
                {"detail": f"Error while booking seat: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


class CancelBookingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        security=[{'Bearer': []}],
        responses={200: openapi.Response("Booking cancelled")}
    )
    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)

        if booking.user != request.user:
            return Response(
                {"detail": "You cannot cancel another user's booking."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if booking.status == Booking.STATUS_CANCELLED:
            return Response(
                {"detail": "Booking is already cancelled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        booking.status = Booking.STATUS_CANCELLED
        booking.save()

        return Response(
            {"detail": "Booking cancelled successfully."},
            status=status.HTTP_200_OK,
        )


class MyBookingsListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(security=[{'Bearer': []}])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by("-created_at")
