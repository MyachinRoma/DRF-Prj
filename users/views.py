from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.filters import OrderingFilter
from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
from users.services import (
    create_stripe_product,
    create_stripe_price,
    create_stripe_checkout_sessions,
)


class MixinQueryset:
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user.pk)
        return queryset


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = (
        "paid_course",
        "paid_lesson",
        "payment_method",
    )
    ordering_fields = ("payment_date",)


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save()
        if payment.paid_course:
            product_name = f"{payment.paid_course.title} Course"
        else:
            product_name = "General Course"
        product = create_stripe_product(product_name)
        price = create_stripe_price(payment.payment_amount, product)

        # Создание сессии для оплаты
        session_id, payment_link = create_stripe_checkout_sessions(price)

        # Сохранение данных в модель Payments
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
