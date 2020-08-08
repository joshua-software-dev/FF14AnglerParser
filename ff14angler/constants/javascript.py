#! /usr/bin/env python3

comment_metadata_javascript = """\
comment_element = document.querySelector('.comment_list');
comment_type = comment_element.attributes[1].value;
comment_item = comment_element.attributes[2].value;
for (const small_tag of document.querySelectorAll('.small')) {
    if (small_tag.previousElementSibling.innerText == 'Comments')
    {
        return [RID, comment_type, comment_item, small_tag.innerText];
    }
}"""

