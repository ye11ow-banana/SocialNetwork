from reader import read_config
from services import signup_users_and_create_posts, create_likes_randomly


def main() -> None:
    config = read_config('config.yaml')
    access_tokens, posts = signup_users_and_create_posts(
        config.number_of_users, config.max_posts_per_user
    )
    max_likes_per_user = config.max_likes_per_user
    if len(posts) < max_likes_per_user:
        max_likes_per_user = len(posts)
    create_likes_randomly(access_tokens, posts, max_likes_per_user)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(str(e))
