class UserService:
    @staticmethod
    def update(user, data: dict):
        for k, v in data.items():
            setattr(user, k, v)

        user.save()
        return user
