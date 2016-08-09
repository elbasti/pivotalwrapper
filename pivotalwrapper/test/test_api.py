import pytest
import re

from pivotalwrapper.api import PivotalConnection


# Fixtures
@pytest.fixture
def connection():
    return PivotalConnection(project_id='test_project', token='test_token')

@pytest.fixture
def mocked_connection(mocker):
    PEOPLE = [{'person': {'email': 'foo1@bar.com', 'id': 1}},
              {'person': {'email': 'foo2@bar.com', 'id': 2}},
              {'person': {'email': 'foo3@bar.com', 'id': 3}}]

    mocker.patch.object(PivotalConnection, 'get', return_value=PEOPLE)
    return PivotalConnection(project_id='test_project', token='test_token')

## Tests

# Constructor Tests
def test_requires_project_id_and_token():
    with pytest.raises(ValueError) as excinfo:
        c = PivotalConnection()
    assert 'Project id and token are required' in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        c = PivotalConnection(token='a')
    assert 'Project id and token are required' in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        c = PivotalConnection(project_id='b')
    assert 'Project id and token are required' in str(excinfo.value)

    c = PivotalConnection(project_id = 'b', token = 'a')
    assert c is not None



# Endpoint tests

def test_endpoint_has_correct_base_url(connection):
    endpoint = connection.Endpoint(connection)
    assert endpoint._base_endpoint == \
            'https://www.pivotaltracker.com/services/v5/projects/test_project'

def test_endpoint_builds_urls(connection):
    endpoint = connection.Endpoint(connection)
    endpoint.resource('story')
    endpoint.with_state('started')
    endpoint.with_state('finished')

    assert endpoint._endpoint == \
            'https://www.pivotaltracker.com/services/v5/projects/test_project/'\
            'story?with_state=started&with_state=finished'
            
def test_gets_person(mocked_connection):
    person = mocked_connection.get_person('1')
    assert person == {'email': 'foo1@bar.com', 'id': 1}
