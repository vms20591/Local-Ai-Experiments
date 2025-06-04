import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import builtins
import uuid
from types import SimpleNamespace

class DummyMessagesPlaceholder:
    def __init__(self, *args, **kwargs):
        pass

class DummyPromptTemplate:
    @classmethod
    def from_messages(cls, msgs):
        return cls()

    def __or__(self, other):
        return other

sys.modules.setdefault(
    "langchain.prompts",
    SimpleNamespace(MessagesPlaceholder=DummyMessagesPlaceholder, ChatPromptTemplate=DummyPromptTemplate),
)
sys.modules.setdefault(
    "langchain_core.runnables.history",
    SimpleNamespace(RunnableWithMessageHistory=object),
)
sys.modules.setdefault(
    "langchain_openai",
    SimpleNamespace(ChatOpenAI=object),
)
sys.modules.setdefault(
    "langchain_mongodb",
    SimpleNamespace(MongoDBChatMessageHistory=object),
)
sys.modules.setdefault(
    "colorama",
    SimpleNamespace(
        init=lambda *a, **k: None,
        Style=SimpleNamespace(BRIGHT="", RESET_ALL=""),
        Fore=SimpleNamespace(GREEN="", BLUE="", YELLOW="", RED=""),
    ),
)

import pytest

import app


class DummyChain:
    def __init__(self, captured):
        self.captured = captured

    def stream(self, *args, **kwargs):
        self.captured['session_id'] = kwargs['config']['configurable']['session_id']
        raise KeyboardInterrupt


@pytest.fixture(autouse=True)
def patch_dependencies(monkeypatch):
    monkeypatch.setattr(app, 'ChatOpenAI', lambda **kw: object())
    monkeypatch.setattr(app, 'MongoDBChatMessageHistory', lambda **kw: object())

    captured = {}

    def make_dummy_chain(chain, get_session_history, input_messages_key, history_messages_key):
        return DummyChain(captured)

    monkeypatch.setattr(app, 'RunnableWithMessageHistory', make_dummy_chain)

    yield captured


def run_app_with_args(monkeypatch, args):
    monkeypatch.setattr(sys, 'argv', ['app.py'] + args)
    monkeypatch.setattr(builtins, 'input', lambda _: 'hi')
    with pytest.raises(SystemExit):
        app.main()


def test_valid_uuid(monkeypatch, patch_dependencies):
    valid = str(uuid.uuid4())
    run_app_with_args(monkeypatch, [valid])
    assert patch_dependencies['session_id'] == valid


def test_invalid_uuid(monkeypatch, patch_dependencies):
    invalid = 'not-a-valid-uuid'
    run_app_with_args(monkeypatch, [invalid])
    captured = patch_dependencies['session_id']
    uuid_obj = uuid.UUID(captured)
    assert str(uuid_obj) == captured
    assert captured != invalid
