#coding=utf-8
def parser(file_path):
    blog_dict = {}
    blog = open(file_path, 'rU').read()
    # Title
    title_start = blog.find("TITLE:") + 6
    title_end = blog.find("**", title_start)
    title = unicode(blog[title_start:title_end], 'utf-8')
    blog_dict.setdefault('title', title)

    # Classify
    classify_start = blog.find("CLASSIFY:") + 9
    classify_end = blog.find("**", classify_start)
    classify = unicode(blog[classify_start: classify_end], 'utf-8')
    blog_dict.setdefault("classify", classify)

    # Keywords
    keywords_start = blog.find("KEYWORDS:") + 9
    keywords_end = blog.find("**", keywords_start)
    keywords = unicode(blog[keywords_start:keywords_end], 'utf-8')
    blog_dict.setdefault("keywords", keywords)

    # Music
    music_start = blog.find("MUSIC:") + 6
    music_end = blog.find("**", music_start)
    music = "null"
    if music_start > 5:  #如果不存在，blog_start=-1, blog_start+5 = -1
        music = blog[music_start: music_end]
    blog_dict.setdefault("music", music)

    # Content
    content_start = blog.find("------") + 7
    content_end = len(blog)
    content = unicode(blog[content_start:content_end], 'utf-8')
    blog_dict.setdefault("content", content)
    print blog_dict

    return blog_dict


if __name__ == '__main__':
    file_path = 'C:/Users/zhouy/Desktop/123.md'
    parser(file_path)

