class UserService:
    @staticmethod
    def update(user, data: dict):
        password = None
        if 'password' in data:
            password = data.pop('password')
        for k, v in data.items():
            setattr(user, k, v)

        if password:
            user.set_password(password)
        user.save()
        return user
