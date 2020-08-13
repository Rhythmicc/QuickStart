# coding=utf-8
from QuickStart_Rhy.API import *
import qiniu


class QiniuOSS:
    def __init__(self, ac_key=pre_check('qiniu_ac_key'),
                 sc_key=pre_check('qiniu_sc_key'),
                 df_bucket=pre_check('qiniu_bk_name')):
        """
        初始化并登陆七牛云对象存储

        Initializes and logs in qiniu cloud object storage

        :param ac_key: Access Key
        :param sc_key: Secret Key
        :param df_bucket: 默认桶名称
        """
        self.ac_key = ac_key
        self.sc_key = sc_key
        self.auth = qiniu.Auth(self.ac_key, self.sc_key)
        self.df_bucket = df_bucket

    def get_func_table(self):
        """
        获取对象支持的操作

        Gets the operations supported by the object

        :return: 函数表
        """
        return {
            '-up': self.upload,
            '-rm': self.remove,
            '-cp': self.copy_url,
            '-dl': self.download,
            '-ls': self.list_bucket
        }

    def upload(self, filePath: str, bucket=None):
        """
        上传文件

        Upload file

        :param filePath: 文件路径
        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        tk = self.auth.upload_token(bucket if bucket else self.df_bucket, filePath.split(dir_char)[-1])
        qiniu.put_file(tk, filePath.split(dir_char)[-1], filePath)

    def remove(self, filePath: str, bucket=None):
        """
        删除文件

        Delete file

        :param filePath: 文件路径（对象存储中）
        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        bk = qiniu.BucketManager(self.auth)
        bk.delete(bucket if bucket else self.df_bucket, filePath)

    def copy_url(self, filePath: str, bucket=None):
        """
        通过url拷贝文件（这个接口貌似没有卵用，七牛云那边并不会生效）

        Copy files through URL (this interface seems to have no egg use, qiniu cloud will not work)

        :param filePath: 文件链接
        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        bk = qiniu.BucketManager(self.auth)
        bk.fetch(filePath, bucket if bucket else self.df_bucket, filePath.split('/')[-1])

    def get_bucket_url(self, bucket=None):
        """
        获取当前桶的访问链接

        Gets the access link for the current bucket

        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: 成功返回json，否则False
        """
        import requests
        bucket = bucket if bucket else self.df_bucket
        url = 'http://api.qiniu.com/v6/domain/list?tbl=%s' % bucket
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "QBox %s" % self.auth.token_of_request(url)
        }
        res = requests.get(url, headers=headers)
        if res.status_code == requests.codes.ok:
            return res.json()
        else:
            return False

    def list_bucket(self, bucket=None):
        """
        展示bucket中所有的文件

        Displays all the files in the bucket

        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        from prettytable import PrettyTable
        bk = qiniu.BucketManager(self.auth)
        ret = bk.list(bucket if bucket else self.df_bucket)
        if not ret[1]:
            print("ERROR!")
            exit(0)
        root_url = 'http://' + self.get_bucket_url(bucket)[0] + '/'
        ret = ret[0]['items']
        from QuickStart_Rhy.NetTools.NormalDL import size_format
        tb = PrettyTable(['File', 'Size'])
        for i in ret:
            tb.add_row([i['key'], size_format(i['fsize'], True)])
        print("Bucket url:", root_url)
        print(tb)

    def download(self, filePath: str, bucket=None):
        """
        下载文件

        Download file

        :param filePath: 文件在桶中的路径
        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        from QuickStart_Rhy.NetTools.NormalDL import normal_dl
        bucket = bucket if bucket else self.df_bucket
        root_url = self.get_bucket_url(bucket)[0]
        if root_url:
            root_url = 'http://' + root_url + '/'
        else:
            exit('Get Bucket Url Failed!')
        dl_url = root_url + filePath
        if bucket.startswith('admin'):
            dl_url = self.auth.private_download_url(dl_url)
        normal_dl(dl_url)