import re
import unicodedata

import sublime
import sublime_plugin

replacements = [
    [r"[’‘′‚]", "'"],
    [r"[“”″„]", '"'],
    [r"[…]", "..."],
    [r"[—]", "---"],
    [r"[–]", "--"],
    [r"[•]", "*"],
    [r"[·]", "-"],
    [r"[ ]", "   "],
    [r"[ ]", "  "],
    [r"[   ]", " "],
    [r"[«]", "<<"],
    [r"[»]", ">>"],
    [r"[©]", "(C)"],
    [r"[®]", "(R)"],
    [r"[™]", "(TM)"],
]


def convert_to_ascii(string):
    return unicodedata.normalize("NFKD", string).encode("ascii", "ignore").decode("ascii")


def selections(view):
    regions = [r for r in view.sel() if not r.empty()]
    if not regions:
        regions = [sublime.Region(0, view.size())]
    return regions


class ReplaceNonAsciiCharactersCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        has_changes = False

        for region in selections(view):
            source_text = view.substr(region)
            if len(source_text) > 0:
                string = source_text
                # replace smart characters
                for pattern, repl in replacements:
                    string = re.sub(pattern, repl, string)
                # normalize non-ascii characters
                replaced_text = convert_to_ascii(string)
                # check for changes
                if source_text != replaced_text:
                    view.replace(edit, region, replaced_text)
                    has_changes = True

        if has_changes:
            sublime.status_message("TextConverter: non-ASCII characters replaced")
        else:
            sublime.status_message("TextConverter: no changes")
