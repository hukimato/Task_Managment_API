from djoser import email
from django.conf import settings


class ConfirmationEmail(email.ConfirmationEmail):
    template_name = 'email/confirmation.html'


class PasswordResetEmail(email.PasswordResetEmail):
    template_name = 'email/password_reset.html'

    def get_context_data(self):
        # PasswordResetEmail can be deleted
        context = super().get_context_data()
        context["frontend_url"] = settings.FRONTEND_URL
        print(settings.FRONTEND_URL)
        return context