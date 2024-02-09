from django.contrib.auth.models import BaseUserManager


class AuthUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Utilizatorul trebuie sa aiba o adresa de email.")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_superuser = False
        user.is_staff = False
        user.save(using=self._db)

        return user