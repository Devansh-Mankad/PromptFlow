import uuid
class SessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self) -> str:
        session_id = str(
            uuid.uuid4()
        )
        self.sessions[
            session_id
        ] = {
            "history": [],
            "last_response": ""
        }
        return session_id

    def get_session(self,session_id: str):
        if (
            session_id
            not in self.sessions
        ):
            self.sessions[
                session_id
            ] = {
                "history": [],
                "last_response": ""
            }

        return self.sessions[
            session_id
        ]

    def get_history(self,session_id: str):
        return self.get_session(
            session_id
        )["history"]

    def set_history(self,session_id: str,history: list):
        self.get_session(
            session_id
        )["history"] = history

    def get_last_response(self,session_id: str):
        return self.get_session(
            session_id
        )["last_response"]

    def set_last_response(self,session_id: str,response: str):
        self.get_session(
            session_id
        )[
            "last_response"
        ] = response

    def clear_session(self,session_id: str):
        self.sessions[
            session_id
        ] = {
            "history": [],
            "last_response": ""
        }

    def delete_session(self,session_id: str):
        if (
            session_id
            in self.sessions
        ):
            del self.sessions[
                session_id
            ]

session_manager = (
    SessionManager()
)