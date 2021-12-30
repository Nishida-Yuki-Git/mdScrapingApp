from prefect import Flow, task
from mainJobBatch.taskManage.task.mdScrapingTask import MdScrapingTaskExecute

@task
def jobExecute(user_id):
    md_scraping_job_batch = MdScrapingTaskExecute(user_id)
    md_scraping_job_batch.jobControl()

def goFlow(user_id):
    with Flow("GoScraping") as flow:
        jobExecute(user_id)
    flow.run()