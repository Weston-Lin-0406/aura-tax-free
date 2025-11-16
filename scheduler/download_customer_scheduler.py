from pyfk import SimpleScheduler, get_logger
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor

from library.dao import Customer, CustomerDao, LineChatDao
from library.line_bot_config import LineBotConfig

from linebot import LineBotApi

download_customer_scheduler = SimpleScheduler(
    logger="schedulerLogger",
    executors={
        "default": ThreadPoolExecutor(1),
        "processpool": ProcessPoolExecutor(1)
    },
    job_defaults={
        "coalesce": False,
        "max_instances": 1
    }
)

log = get_logger("schedulerLogger")

@download_customer_scheduler.scheduled_job(id="download_customer_scheduler", trigger="interval", minutes=20)
def process():
    chat_dao = LineChatDao()
    log.info("Query user ids not downloaded.")
    user_ids = chat_dao.get_user_not_download()
    log.info("User ids: %s", repr(user_ids))
    config = LineBotConfig()
    log.info("Initial LineBotApi.")
    line_bot_api = LineBotApi(config.get_token())
    customer_list = []
    log.info("Start download user profile.")
    for user_id in user_ids:
        profile = line_bot_api.get_profile(user_id)
        customer = Customer(user_id, profile.display_name, profile.picture_url)
        customer_list.append(customer)
        log.info("Get profile: %s", repr(customer))

    log.info("Insert into DB.")
    customer_dao = CustomerDao()
    customer_dao.create_batch(customer_list)
        