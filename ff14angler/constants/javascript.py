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

# noinspection SpellCheckingInspection
fetch_large_url_data_from_lodestone_page = """\
function toDataURL(url, callback)
{
    var xhr = new XMLHttpRequest();
    xhr.open('get', url);
    xhr.responseType = 'blob';
    xhr.onload = function()
    {
        var fr = new FileReader();
        fr.onload = function()
        {
            callback(this.result);
        };
        fr.readAsDataURL(xhr.response);
    }
    xhr.send();
}

toDataURL(
    document.querySelector('.db-view__item__icon__item_image.sys_nq_element').src,
    arguments[arguments.length - 1]
)"""
