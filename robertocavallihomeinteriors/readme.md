### 解决 WARNING: File (code: 302): Error downloading file from
`settings.py` 增加 `MEDIA_ALLOW_REDIRECTS = True`配置项

### 增加下载文件重命名和保存路径
```python
class FileDownloadPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        media_requests = super(FileDownloadPipeline, self).get_media_requests(item, info)
        for media_request in media_requests:
            media_request.item = item
            # print('{0}的文件正在下载中.....'.format(item['title']))
        return media_requests

    def file_path(self, request, response=None, info=None):
        # 获取默认保存的文件路径
        origin_path = super(FileDownloadPipeline, self).file_path(request, response, info)
        # 过滤文件夹非法字符串
        title = re.sub(r'[\\/:\*\?"<>\|]', "", request.item['title'])
        # 修改保存文件夹路径
        save_path = origin_path.replace("full", title)
        # 重命名文件名
        for i in request.item['files']:
            if i['pdf_url'] == request.url:
                print('{0}的文件{1}正在下载中.....'.format(title, i['pdf_name']))
                return re.sub(r'\b[0-9a-f]{40}\b', i['pdf_name'] + '_' + str(int(round(time.time() * 1000))),
                              save_path)
        return origin_path
```