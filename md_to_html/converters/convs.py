import re

class BaseConverter:
    def __init__(self, text):
        self.result_text = "<p>"+text+"</p>"

    def to_html(self):
        return self.result_text
    

class LinkConverter(BaseConverter):
    def __init__(self, text):
        # Regex for markdown links
        pattern = r"\[([^\]]+)\]\(([^)]+)\)"
        
        # html link format
        replacement = r'<a href="\2">\1</a>'
        
        # replace markdown links with HTML links
        self.result_text = re.sub(pattern, replacement, text)


class StrictConverter(BaseConverter):
    def __init__(self, text):
        self.result_text =  text
        self.valid = False
        self.internals = [LinkConverter]
    
    def is_valid(self):
        return self.valid
    
    def to_html(self):
        # run non-strict converters inside result text
        for internal in self.internals:
            internal_proc = internal(self.result_text)
            self.result_text = internal_proc.to_html()

        return self.result_text
    
class NoopConverter(StrictConverter):
    def __init__(self, text):
        super().__init__(text)
        self.result_text =  "<p>"+text+"</p>"
        self.valid = True
    
    def is_valid(self):
        return self.valid
    
    def to_html(self):
        # run non-strict converters inside result text
        for internal in self.internals:
            internal_proc = internal(self.result_text)
            self.result_text = internal_proc.to_html()

        return self.result_text
    
class HeadingConverter(StrictConverter):
    def __init__(self, text):
        super().__init__(text)
        
        # pattern for heading md symbols
        pattern = r"^\s{0,3}(#{1,6})\s+(.*)$"

        match = re.match(pattern, text)
        
        if match:
            self.valid = True
            level = len(match.group(1))  
            heading_tag = "h"+str(level)
            heading_text = match.group(2)
            self.result_text = "<"+heading_tag+">"+heading_text+"</"+heading_tag+">"


class MdProcessor:
    
    def __init__(self):
        self.checks = [HeadingConverter]
        self.previous = ""
        self.result = []

    # private function to check for any text in stored texts
    # then add them into result and clear stored text
    def _check_previous(self):
        self.previous = self.previous.strip()
        if len(self.previous) > 0:
            conv = NoopConverter(self.previous)
            self.result.append(conv.to_html())
        self.previous = ""

    # check the passed in text. 
    def check_append(self, line):
        valid = False
        for check in self.checks:
            ch_obj = check(line)
            if ch_obj.is_valid():
                # the current line has a valid md tag

                # we need to check stored text and add it to result list
                self._check_previous()

                # add the converted line to result list
                valid = True
                self.result.append(ch_obj.to_html())
                break

        if line.strip() == "":
            # line is empty string, we need to clear stored text and add it to <p>
            self._check_previous()
        elif not valid:
            # if the line does not have strict tags then add it to stored text
            self.previous = self.previous + line.strip() + "\n"

    # formally finish processing the md texts.
    # double check any left over in stored texts
    # return result list
    def finish(self, check_leftover = True):
        if check_leftover:
            self._check_previous()
        return self.result
