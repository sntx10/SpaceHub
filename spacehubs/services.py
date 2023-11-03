from django.contrib.auth import get_user_model

from spacehubs.models import News, Project, Blog, PodCast, Post, ProjectView, BlogView, PostView, PodCastView, NewsView

# Create your recommended here.

User = get_user_model()


def get_latest_news(user):
    """
    Получает последние новости, упорядоченные по дате публикации.
    :param user: Аутентифицированный пользователь (не используется в этой функции, но может быть полезен для будущих расширений).
    :return: QuerySet новостей, упорядоченных по дате публикации.
    """
    return News.objects.all().order_by('-expanded_date_posted')


def get_recommended_project(user):
    """
    Получает рекомендованные проекты на основе предпочтений пользователя.
    :param user: Аутентифицированный пользователь.
    :return: QuerySet рекомендованных проектов или все проекты, если у пользователя нет предпочтений.
    """
    if user.preferences.exists():
        return Project.objects.filter(category__in=user.preferences.all())
    return Project.objects.all()


def get_recommended_blog(user):
    """
    Получает рекомендованные блоги на основе предпочтений пользователя.
    :param user: Аутентифицированный пользователь.
    :return: QuerySet рекомендованных блогов или все блоги, если у пользователя нет предпочтений.
    """
    if user.preferences.exists():
        return Blog.objects.filter(category__in=user.preferences.all())
    return Blog.objects.all()


def get_recommended_post(user):
    """
    Получает рекомендованные посты на основе предпочтений пользователя.
    :param user: Аутентифицированный пользователь.
    :return: QuerySet рекомендованных постов или все посты, если у пользователя нет предпочтений.
    """
    if user.preferences.exists():
        return Post.objects.filter(category__in=user.preferences.all())
    return Post.objects.all()


def get_recommended_podcast(user):
    """
    Получает рекомендованные подкасты на основе предпочтений пользователя.
    :param user: Аутентифицированный пользователь.
    :return: QuerySet рекомендованных подкастов или все подкасты, если у пользователя нет предпочтений.
    """
    if user.preferences.exists():
        return PodCast.objects.filter(category__in=user.preferences.all())
    return PodCast.objects.all()


def add_project_view(user, project):
    """
    Увеличивает счетчик просмотров проекта, если пользователь не просматривал его ранее.
    :param user: Аутентифицированный пользователь.
    :param project: Объект проекта.
    """
    if ProjectView.objects.filter(user=user, project=project).exists():
        return

    ProjectView.objects.create(user=user, project=project)
    project.views_count += 1
    project.save()


def add_blog_view(user, blog):
    """
    Увеличивает счетчик просмотров блога, если пользователь не просматривал его ранее.
    :param user: Аутентифицированный пользователь.
    :param blog: Объект блога.
    """
    if BlogView.objects.filter(user=user, blog=blog).exists():
        return

    BlogView.objects.create(user=user, blog=blog)
    blog.views_count += 1
    blog.save()


def add_post_view(user, post):
    """
    Увеличивает счетчик просмотров поста, если пользователь не просматривал его ранее.
    :param user: Аутентифицированный пользователь.
    :param post: Объект поста.
    """
    if PostView.objects.filter(user=user, post=post).exists():
        return

    PostView.objects.create(user=user, post=post)
    post.views_count += 1
    post.save()


def add_podcast_view(user, podcast):
    """
    Увеличивает счетчик просмотров подкаста, если пользователь не просматривал его ранее.
    :param user: Аутентифицированный пользователь.
    :param podcast: Объект подкаста.
    """
    if PodCastView.objects.filter(user=user, podcast=podcast).exists():
        return

    PodCastView.objects.create(user=user, podcast=podcast)
    podcast.views_count += 1
    podcast.save()


def add_news_view(user, news):
    """
    Увеличивает счетчик просмотров новости, если пользователь не просматривал ее ранее.
    :param user: Аутентифицированный пользователь.
    :param news: Объект новости.
    """
    if NewsView.objects.filter(user=user, news=news).exists():
        return

    NewsView.objects.create(user=user, news=news)
    news.views_count += 1
    news.save()



