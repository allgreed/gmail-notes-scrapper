import pytest
from main import parse_note_body


@pytest.mark.parametrize("note_body, expected_result", [
    ('<html><head></head><body style="overflow-wrap: break-word; -webkit-nbsp-mode: space; line-break: after-white-space;"><a href="https://news.ycombinator.com/item?id=42664526">https://news.ycombinator.com/item?id=42664526</a></body></html',
     'https://news.ycombinator.com/item?id=42664526'),
    ('<html><head></head><body style="overflow-wrap: break-word; -webkit-nbsp-mode: space; line-break: after-white-space;">Archive&nbsp;<a href="https://rustle.ca/posts/articles/work-from-home-lighting">https://rustle.ca/posts/articles/work-from-home-lighting</a></body></html>',
     'Archive https://rustle.ca/posts/articles/work-from-home-lighting'),
    ('<html><head></head><body style="overflow-wrap: break-word; -webkit-nbsp-mode: space; line-break: after-white-space;">Quote:&nbsp;<span style="-webkit-text-size-adjust: auto; caret-color: rgb(51, 51, 51); color: rgb(51, 51, 51); font-family: sans-serif; font-size: 16.200001px;">r. When working with someone on a project don\'t "design an interface" and then work alone on either side of it. Work together all over it.</span></body></html>',
     'Quote: r. When working with someone on a project don\'t "design an interface" and then work alone on either side of it. Work together all over it.',
     )
])
def test_parse_note_body(note_body, expected_result):
    assert parse_note_body(note_body) == expected_result

