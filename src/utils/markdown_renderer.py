"""Markdown to HTML renderer using mistune."""
import mistune


class MarkdownRenderer(mistune.HTMLRenderer):
    def __init__(self):
        super().__init__(escape=False)

    def heading(self, text, level):
        return f'<h{level} style="margin: 16px 0 8px; color: palette(text);">{text}</h{level}>'

    def paragraph(self, text):
        return f'<p style="margin: 8px 0; line-height: 1.6;">{text}</p>'

    def list(self, text, ordered, level, start=None):
        tag = 'ol' if ordered else 'ul'
        style = 'margin: 8px 0; padding-left: 24px;'
        return f'<{tag} start="{start}" style="{style}">{text}</{tag}>' if start and ordered else f'<{tag} style="{style}">{text}</{tag}>'

    def list_item(self, text, level):
        return f'<li style="margin: 4px 0;">{text}</li>'

    def block_code(self, code, info=None):
        lang = f' class="language-{info}"' if info else ''
        return f'<pre style="background: #1e1e1e; padding: 12px; border-radius: 6px; overflow-x: auto;"><code{lang} style="color: #d4d4d4; font-family: Consolas, monospace;">{code}</code></pre>'

    def codespan(self, text):
        return f'<code style="background: #2d2d2d; padding: 2px 6px; border-radius: 3px; color: #ce9178; font-family: Consolas, monospace;">{text}</code>'

    def link(self, text, url, title=None):
        return f'<a href="{url}" title="{title or ""}" style="color: #3794ff; text-decoration: none;">{text}</a>'

    def emphasis(self, text):
        return f'<em style="font-style: italic;">{text}</em>'

    def strong(self, text):
        return f'<strong style="font-weight: 600;">{text}</strong>'

    def thematic_break(self):
        return '<hr style="border: none; border-top: 1px solid #404040; margin: 16px 0;">'

    def block_quote(self, text):
        return f'<blockquote style="border-left: 4px solid #404040; padding-left: 16px; margin: 8px 0; color: #808080;">{text}</blockquote>'

    def table(self, text):
        return f'<table style="border-collapse: collapse; width: 100%; margin: 8px 0;">{text}</table>'

    def table_head(self, text):
        return f'<thead>{text}</thead>'

    def table_body(self, text):
        return f'<tbody>{text}</tbody>'

    def table_row(self, text):
        return f'<tr style="border-bottom: 1px solid #404040;">{text}</tr>'

    def table_cell(self, text, align, is_head):
        tag = 'th' if is_head else 'td'
        align_style = f' text-align: {align};' if align else ''
        return f'<{tag} style="padding: 8px; border: 1px solid #404040;{align_style}">{text}</{tag}>'


def render_markdown(content: str) -> str:
    renderer = MarkdownRenderer()
    markdown = mistune.Markdown(renderer=renderer)
    body = markdown(content)
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                font-size: 14px;
                line-height: 1.6;
                padding: 20px;
                margin: 0;
            }}
            img {{ max-width: 100%; height: auto; border-radius: 4px; }}
        </style>
    </head>
    <body>{body}</body>
    </html>
    """
