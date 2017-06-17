### 名称

scan_all_class_reference.py

### 功能

* 统计目录下全部 Objective-C 文件引用外部类

### 介绍

* 遍历对应目录中下全部 .h .m 文件；
* 识别主类以及该主类所引用全部外部类；
* 输出 output 结果文件，该文件夹下包含 class_reference.json 与 class_reference.index 两个文件，以便提供不同查阅方法。

```javascript
[
    {
        "main": "classname",
        "path": "path",
        "sub": [
            {
                "name": "classname",
                "type": "",
                "position": ""
            },
            ...
        ]
    },
    ...
]
```

### 使用

```shell
usage:

$ python scan_all_class_reference.py -i project_path

-i <optional : input project path, default is current folder>
```

![scan_all_files_in_project_1](Resource/scan_all_files_in_project_1.png)
![scan_all_files_in_project_2](Resource/scan_all_files_in_project_2.png)