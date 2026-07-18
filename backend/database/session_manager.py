import uuid

# Temporary in-memory session storage
_sessions = {}


def create_session(data):
    """
    Create a new session and store the provided data.

    Parameters:
        data (dict): Repository data to store.

    Returns:
        str: Generated session ID.
    """

    session_id = str(uuid.uuid4())
    _sessions[session_id] = data

    return session_id


def get_session(session_id):
    """
    Retrieve a session by its ID.

    Parameters:
        session_id (str)

    Returns:
        dict | None: Session data if found, otherwise None.
    """

    return _sessions.get(session_id)


def delete_session(session_id):
    """
    Delete a session.

    Parameters:
        session_id (str)

    Returns:
        bool: True if deleted, False otherwise.
    """

    return _sessions.pop(session_id, None) is not None