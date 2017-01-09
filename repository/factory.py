"""
Factory for different types of repositories.

"""


def create_repository(config):
    """Creates a repository from its name and settings.
    """
    if config.REPOSITORY_NAME == 'mongodb':
        from repository.mongodb import MongoDBRepository
        auth = None
        if config.MONGODB_USEAUTH:
            auth = (config.MONGODB_USERNAME, config.MONGODB_PASSWORD)
        return MongoDBRepository(host_name=config.MONGODB_HOST,
                                 database_name=config.MONGODB_DATABASE,
                                 collection_name=config.MONGODB_COLLECTION,
                                 auth=auth)
    # elif config.REPOSITORY_NAME == 'mysql':
    #    from repository.mysql import Repository
    else:
        raise ValueError('Unknown repository.')

        # return Repository(config)
