def pass_gen():
    import random, string # pylint: disable=import-outside-toplevel,multiple-imports
    return ''.join(random.choice(string.ascii_letters) for i in range(30))

def is_over_website_limit(user):
    from namelessmc_hosting import settings
    from .models import Website, Account

    if user.is_superuser:
        return False

    user_website_count = len(Website.objects.filter(owner=user))
    num_credit = Account.objects.filter(user=user).first().credit
    website_count_limit = settings.USER_MAX_WEBSITES if num_credit > settings.USER_PAID_MINIMUM_CREDITS else settings.USER_MAX_FREE_WEBSITES
    return user_website_count >= website_count_limit
