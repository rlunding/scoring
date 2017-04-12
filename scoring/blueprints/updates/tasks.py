from scoring.app import create_celery_app

celery = create_celery_app()


@celery.task()
def retrieve_new_scores():
    """
    Retrieve scores from peers

    :return: None
    """
    pass
