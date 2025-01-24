import pytest
from main import parse_note_body


@pytest.mark.parametrize("note_body, expected_result", [
    ('<html><head></head><body style="overflow-wrap: break-word; -webkit-nbsp-mode: space; line-break: after-white-space;"><a href="https://news.ycombinator.com/item?id=42664526">https://news.ycombinator.com/item?id=42664526</a></body></html',
     'https://news.ycombinator.com/item?id=42664526'),
    ('<html><head></head><body style="overflow-wrap: break-word; -webkit-nbsp-mode: space; line-break: after-white-space;">Archive&nbsp;<a href="https://rustle.ca/posts/articles/work-from-home-lighting">https://rustle.ca/posts/articles/work-from-home-lighting</a></body></html>',
     'Archive https://rustle.ca/posts/articles/work-from-home-lighting'),
])
def test_parse_note_body(note_body, expected_result):
    assert parse_note_body(note_body) == expected_result
