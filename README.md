# PivotalWrapper

This is a simple wrapper for fetching stories &amp; people information from pivotal tracker.

## Requirements
Built and tested with python 3.5

## Installation
After cloning, run `pip install -e .` from the project root.

## Running tests
Tests require pytest

In the project root type `py.test`

## Usage

### Basic usage

Create a pivotal connection:
    

    from pivotalwrapper.api import PivotalConnection

    # Initialize a connection object
    connection = PivotalConnection(project_id='my_id', token='my_token')
    
    # Connections need a resource
    connection.resource('story')

    # Get a response by calling get() on your connection
    response = connection.get()

    # You can also chain them together:
    response = connection.resource('story').with_state('started').get()

### Convenience methods
A couple convenience methods are provided:
    
- `get_started_stories()` will return all started stories (obvs)
- `get_person(id)` will return all the details of a member with a given id

