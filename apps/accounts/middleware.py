from .services import update_user_last_activity


class UpdateLastActivityMiddleware:
    """
    Monitors each request and updates user last activity time.
    """

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)
        try:
            user = request.user
        except AttributeError:
            raise AttributeError(
                'The UpdateLastActivityMiddleware requires '
                'authentication middleware to be installed.'
            )
        if user.is_authenticated:
            update_user_last_activity(user.id)
        return response
