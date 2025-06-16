import unittest
import tempfile
import os
from pathlib import Path
from raindropMD import (
    Bookmark, bookmarks_to_markdown, write_markdown, parse_markdown_file,
    parse_raindrop_csv, sanitize_title, zettelkasten_filename,
    write_bookmarks_to_dir, print_bookmarks_from_dir,
    remove_bookmark_interactive_dir, edit_bookmark_interactive_dir,
    fuzzy_search_bookmarks_dir
)

class TestRaindropCSVToMarkdown(unittest.TestCase):
    def setUp(self):
        # Example CSV content
        self.csv_content = (
            "id,title,note,excerpt,url,tags,created,cover,highlights,favorite\n"
            "1,Test Title,,Excerpt text,http://example.com,tag1,2025-01-01,,Highlight:Highlight 1,true\n"
        )
        self.csv_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.csv')
        self.csv_file.write(self.csv_content)
        self.csv_file.close()

        # Directory for bookmark files
        self.bookmark_dir = tempfile.TemporaryDirectory()
        self.bookmark_dir_path = Path(self.bookmark_dir.name)

    def tearDown(self):
        os.unlink(self.csv_file.name)
        self.bookmark_dir.cleanup()

    def test_parse_raindrop_csv(self):
        bookmarks = parse_raindrop_csv(self.csv_file.name)
        self.assertEqual(len(bookmarks), 1)
        self.assertEqual(bookmarks[0].title, 'Test Title')
        self.assertEqual(bookmarks[0].url, 'http://example.com')
        self.assertEqual(bookmarks[0].highlights, 'Highlight:Highlight 1')

    def test_write_bookmarks_to_dir_and_list(self):
        bookmarks = parse_raindrop_csv(self.csv_file.name)
        write_bookmarks_to_dir(bookmarks, self.bookmark_dir_path)
        files = list(self.bookmark_dir_path.glob('*.md'))
        self.assertEqual(len(files), 1)
        with open(files[0], 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('Test Title', content)

    def test_remove_bookmark_interactive_dir(self):
        bookmarks = parse_raindrop_csv(self.csv_file.name)
        write_bookmarks_to_dir(bookmarks, self.bookmark_dir_path)
        import builtins
        orig_input = builtins.input
        builtins.input = lambda _: '1'  # Select first bookmark
        try:
            remove_bookmark_interactive_dir(self.bookmark_dir_path)
            files = list(self.bookmark_dir_path.glob('*.md'))
            self.assertEqual(len(files), 0)
        finally:
            builtins.input = orig_input

    def test_edit_bookmark_interactive_dir(self):
        bookmarks = parse_raindrop_csv(self.csv_file.name)
        write_bookmarks_to_dir(bookmarks, self.bookmark_dir_path)
        import builtins
        orig_input = builtins.input
        # Select first bookmark and change its title
        inputs = iter(['1', 'Edited Title', '', '', '', '', '', '', ''])
        builtins.input = lambda _: next(inputs)
        try:
            edit_bookmark_interactive_dir(self.bookmark_dir_path)
            files = list(self.bookmark_dir_path.glob('*.md'))
            with open(files[0], 'r', encoding='utf-8') as f:
                content = f.read()
            self.assertIn('Edited Title', content)
        finally:
            builtins.input = orig_input

    def test_fuzzy_search_bookmarks_dir(self):
        bookmarks = parse_raindrop_csv(self.csv_file.name)
        write_bookmarks_to_dir(bookmarks, self.bookmark_dir_path)
        import builtins
        orig_print = builtins.print
        output = []
        builtins.print = lambda *args, **kwargs: output.append(' '.join(str(a) for a in args))
        try:
            fuzzy_search_bookmarks_dir(self.bookmark_dir_path, 'test')
            self.assertTrue(any('Test Title' in line for line in output))
            output.clear()
            fuzzy_search_bookmarks_dir(self.bookmark_dir_path, 'nonsensequery')
            self.assertTrue(any('No bookmarks matched the query' in line for line in output))
        finally:
            builtins.print = orig_print

    def test_fuzzy_search_bookmarks_dir_empty(self):
        import builtins
        orig_print = builtins.print
        output = []
        builtins.print = lambda *args, **kwargs: output.append(' '.join(str(a) for a in args))
        try:
            fuzzy_search_bookmarks_dir(self.bookmark_dir_path, 'anything')
            self.assertTrue(any('No bookmark files found' in line for line in output))
        finally:
            builtins.print = orig_print

if __name__ == '__main__':
    unittest.main()
