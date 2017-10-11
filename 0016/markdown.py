#coding:utf-8

import re


class Helper(object):
    """
    1. 自动 wrap markdown 文本中的裸链接
       例如：
           将 `https://www.xxxx.com` 
           转换成 `[https://www.xxxx.com](https://www.xxxx.com)`
    2. 抽取 markdown 文本中图片链接
    """

    def __init__(self, text, img_types = None):

        # 定义图片格式的后缀
        if img_types is not None:
            if isinstance(img_types, str):
                self.img_types = [img_types]
            elif isinstance(img_types, list):
                self.img_types = img_types
            else:
                raise TypeError('img_types must be str or list!')
        else:
            self.img_types = ['png', 'jpg']

        # markdown文本内容
        self.text = text

        # 所有已装饰过的链接起始位置
        self.wrapped_pos = self._get_wrapped_pos()

    def _get_wrapped_pos(self):
        """
        获取已修饰过的链接位置
        返回带有位置信息的list
        """

        # 匹配
        # [...](...)
        # <... src="...">
        # <... href="...">
        wrapped_link_pattern = re.compile(
            r"(?:\[([^\[\]]*?)\]\(|(?:src|href) *= *\")"
            r"(https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])"
            r"(?:\)|\")",
            re.I | re.S,
        )

        # 查找所有链接
        wrapped_pos = []
        def _find_pos(match):
            # 匹配到的子串
            line = match.group()
            for g in match.groups():
                if g:
                    # 分组内容在子串中的偏移量
                    offset = line.index(g)

                    wrapped_pos.append(match.start() + offset)

                    # 将已匹配过的内容替换掉
                    # 避免无法识别[link](link)
                    line = line[:offset] + ' '*len(g) + line[offset+len(g):]

        wrapped_link_pattern.sub(_find_pos, self.text)
        return wrapped_pos

    def _md_wrapper(self, match):
        """
        修饰裸链接
        返回修饰后的链接
        """

        pattern = match.group()
        url = match.groups()[0]

        # 如果链接已修饰，返回匹配的原字符串
        # 否则返回修饰后的字符串
        if match.start() in self.wrapped_pos:
            return pattern
        else:
            return pattern.replace(url, '[{0}]({0})'.format(url))

    def wrap_links(self):
        """
        查找并修饰所有链接
        返回修饰后的文本
        """

        # 匹配所有http/https开头的链接
        link_pattern = re.compile(
            r"(https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])",
            re.I | re.S,
        )
        return link_pattern.sub(self._md_wrapper, self.text)

    def extract_images(self):
        """
        导出图片链接
        返回图片链接的集合
        """

        # 匹配
        # <img src="..."><img>
        # ![...](...)
        img_url_pattern = re.compile(
            r"<img +src *= *{1}(.*?\.(?:{0})){1}>.*?</img>"
            r"|"
            r"!\[.*?\]\((.*?\.(?:{0}))\)".format(
                '|'.join(self.img_types), '(?:"|\')'),
            re.I,
        )
        img_urls = img_url_pattern.findall(self.text)
        return set(map(lambda url: url[0] if url[0] else url[1], img_urls))


if __name__ == '__main__':

    text = '''
    ![aa](1.png) <img src="https://static.xxx.com/static/img/logo_v4.png"></img> ![](https://static.xxx.com/static/img/logo_v1.png)
    Hello World! There is an image: <img src="https://static.xxx.com/static/img/logo_v1.png"></img>
    and There is a link: https://www.google.com/search?q=Hello
    and There is a good link: [https://www.google.com/search?q=Hello](https://www.google.com/search?q=Hello)
    and There is a video: <video src="https://v.qq.com/xyz.mp4"></video>

    extra image:
    false          <img src = 'a.'></img>
    false          <imgsrc = 'b.jpg'></img>
    true           <img  src  =  'c.jpg'></img>
    true           <img src = 'd.jpg'>asdf</img>

    extra link:
    wrap           welcome to http://www.google.com !
    wrap           http://www.google.com
    wrap           welcome to "http://www.google.com"
    wrap           welcome to [http://www.google.com] !
    wrap           welcome to https://www.google.com!
    do not wrap    <a href = "https://www.google.com"></a>
    '''

    h = Helper(text)
    urls = h.extract_images()
    print('-'*30)
    print(h.text)
    print('-'*30)
    print(h.wrap_links())
    print('-'*30)
    for u in urls:
        print('image url:', u)
    print('-'*30)

