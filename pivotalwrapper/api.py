import requests


class PivotalConnection:
    """
    A class to connect to pivotal and parse the response.

    Example:
        # create a connection
        >>> connection = PivotalConnection(project_id = 123)

        # get all stories
        >>> connection.resource('stories').get()
        {'userid1': ['story1', 'story2'], 'userid2':['story4', 'story5']}

    """

    def __init__(self, project_id=None, token=None):
        """A class to connect to pivotal

        Kwargs:
            project_id: The project id for the pivotal
            project you want to connect to.

        """
        self._project_id = project_id
        self._token = token
        self._auth_header = {'X-TrackerToken': self._token}

        if (project_id is None or token is None):
            raise ValueError("Project id and token are required")

    def get_started_stories(self):
        return self.resource('stories').with_state('started').get()

    def get_person(self, _id):
        response = self.resource('memberships').get()

        for member in response:
            if member['person']['id'] == int(_id):
                return member['person']
        return None

    def resource(self, resource):
        endpoint = self.Endpoint(self)
        endpoint.resource(resource)
        return endpoint

    def get(self, endpoint):
        response = requests.get(endpoint, headers=self._auth_header)
        return response.json()

    class Endpoint:
        """
        Class which contains functions to compose pivotal url endpoints

        Example:
            >>> connection = PivotalConnection()
            >>> endpoint = Endpoint(connection)

            >>> print(endpoint.resource('something'))
            http://example.com/something

            >>> print(endpoint.with_state('foo'))
            http://example.com/something?with_state='foo'

            # Calling .get() calls the same method on
            # the PivotalConnection class
            >>> response = endpoint.get()

        """

        def __init__(self, connection):
            self._connection = connection
            self._base_endpoint = \
                'https://www.pivotaltracker.com/services/v5/projects/{}'\
                .format(connection._project_id)
            self._endpoint = self._base_endpoint

        def get(self):
            return self._connection.get(self._endpoint)

        def resource(self, resource):
            self._endpoint += '/' + resource
            return self

        def with_state(self, state):
            if '?' not in self._endpoint:
                self._endpoint += '?'
            else:
                self._endpoint += '&'
            self._endpoint = self._endpoint + 'with_state=' + state
            return self

        def __str__(self):
            return self._endpoint
