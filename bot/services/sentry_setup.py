import sentry_sdk

from bot.settings_reader import config


def sentry_init():
    if config.app_env != "development":
        sentry_sdk.init(
            dsn=config.sentry_dns,
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            traces_sample_rate=0.5,
            # Set profiles_sample_rate to 1.0 to profile 100%
            # of sampled transactions.
            # We recommend adjusting this value in production.
            profiles_sample_rate=0.5,
            send_default_pii=True,
            environment=config.app_env,
        )
