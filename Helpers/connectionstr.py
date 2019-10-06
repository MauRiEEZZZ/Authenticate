def loganalytics(tenant, clientid, secret, workspaceid):
    """
    Concatenate strings into the full loganalytics connection string
    """

    result = '"loganalytics://tenant=\''+tenant+'\';clientid=\''+clientid+'\';clientsecret=\''+secret+'\';workspace=\''+workspaceid+'\';"'

    return result