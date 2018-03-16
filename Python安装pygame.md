# Python安装pygame

注意：安装pygame一定要在 https://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame 下载对应的 系统、位数、以及python的版本

比如说我的python版本是是3.6.2 ，系统是windows 64位

下载的是  pygame-1.9.3-cp36-cp36m-win_amd64.whl

其他的话都会报错

安装
```shell
pip install pygame-1.9.3-cp36-cp36m-win_amd64.whl
```
shell命令检验是否已经安装
```shell
Python 3.6.2 |Anaconda custom (64-bit)| (default, Sep 19 2017, 08:03:39) [MSC v.
1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import pygame
>>> print(pygame.ver)
1.9.3
>>>
```

