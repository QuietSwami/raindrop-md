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
        from raindropMD import get_templates_folder
        base_dir = Path(__file__).parent
        templates_dir = get_templates_folder(base_dir)
        # Use a template for writing bookmarks so frontmatter is present
        template_path = templates_dir / 'bookmark_template.md.j2'
        write_bookmarks_to_dir(bookmarks, self.bookmark_dir_path, template_path)
        import builtins
        orig_input = builtins.input
        builtins.input = lambda *args, **kwargs: '1'  # Accept any args
        try:
            remove_bookmark_interactive_dir(self.bookmark_dir_path)
            files = list(self.bookmark_dir_path.glob('*.md'))
            self.assertEqual(len(files), 0)
        finally:
            builtins.input = orig_input

    def test_edit_bookmark_interactive_dir(self):
        bookmarks = parse_raindrop_csv(self.csv_file.name)
        from raindropMD import get_templates_folder
        base_dir = Path(__file__).parent
        templates_dir = get_templates_folder(base_dir)
        template_path = templates_dir / 'bookmark_template.md.j2'
        write_bookmarks_to_dir(bookmarks, self.bookmark_dir_path, template_path)
        import builtins
        orig_input = builtins.input
        # Select first bookmark and change its title
        inputs = iter(['1', 'Edited Title', '', '', '', '', '', '', ''])
        builtins.input = lambda *args, **kwargs: next(inputs)
        try:
            edit_bookmark_interactive_dir(self.bookmark_dir_path, templates_dir)
            files = list(self.bookmark_dir_path.glob('*.md'))
            with open(files[0], 'r', encoding='utf-8') as f:
                content = f.read()
            self.assertIn('Edited Title', content)
        finally:
            builtins.input = orig_input

    def test_fuzzy_search_bookmarks_dir(self):
        bookmarks = parse_raindrop_csv(self.csv_file.name)
        from raindropMD import get_templates_folder
        base_dir = Path(__file__).parent
        templates_dir = get_templates_folder(base_dir)
        template_path = templates_dir / 'bookmark_template.md.j2'
        write_bookmarks_to_dir(bookmarks, self.bookmark_dir_path, template_path)
        from rich.console import Console as RichConsole
        test_console = RichConsole(record=True)
        import raindropMD
        orig_console = raindropMD.console
        raindropMD.console = test_console
        try:
            raindropMD.fuzzy_search_bookmarks_dir(self.bookmark_dir_path, 'test', templates_dir)
            output = test_console.export_text()
            self.assertIn('Test Title', output)
            test_console.clear()
            raindropMD.fuzzy_search_bookmarks_dir(self.bookmark_dir_path, 'nonsensequery', templates_dir)
            output = test_console.export_text()
            self.assertIn('No bookmarks matched the query', output)
        finally:
            raindropMD.console = orig_console

    def test_fuzzy_search_bookmarks_dir_empty(self):
        from rich.console import Console as RichConsole
        test_console = RichConsole(record=True)
        import raindropMD
        orig_console = raindropMD.console
        raindropMD.console = test_console
        from raindropMD import get_templates_folder
        base_dir = Path(__file__).parent
        templates_dir = get_templates_folder(base_dir)
        try:
            raindropMD.fuzzy_search_bookmarks_dir(self.bookmark_dir_path, 'anything', templates_dir)
            output = test_console.export_text()
            self.assertIn('No bookmark files found', output)
        finally:
            raindropMD.console = orig_console

if __name__ == '__main__':
    unittest.main()
