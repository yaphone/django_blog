#coding=utf-8
def parser(file_path):
    blog_dict = {}
    blog = open(file_path).read()
    # Title
    title_start = blog.find("TITLE:") + 6
    title_end = blog.find("CLASSIFY:") - 1
    title = blog[title_start:title_end]
    blog_dict.setdefault('title', title)

    # Classify
    classify_start = title_end + 10
    classify_end = blog.find("KEYWORDS:") - 1
    classify = blog[classify_start: classify_end]
    blog_dict.setdefault("classify", classify)

    # Keywords
    keywords_start = classify_end + 10
    keywords_end = blog.find("------") - 1
    keywords = blog[keywords_start:keywords_end]
    blog_dict.setdefault("keywords", keywords)

    # Content
    content_start = keywords_end + 7
    content_end = blog.find("******")
    content = blog[content_start:content_end]
    blog_dict.setdefault("content", content)

    return blog_dict


if __name__ == '__main__':
    file = open('/Users/zhouyafeng/Desktop/HelloWorld.md')
    blog = file.read()

