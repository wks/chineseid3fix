# chineseid3fix 

*修复MP3文件里的编码错误的ID3标签*

*Fix ID3 tags with wrong character encodings (especially Chinese)*

# 概述 About

如果你从网上下载MP3文件，尤其是来自中国的MP3文件，那么，里面的ID3元数据很有可能
包 含“乱码”——字符编码错误。

If you download MP3 files from the Internet, especially those MP3 files from
China, chance is high that the ID3 metadata will contain wrongly encoded texts
that display as garbage.

对于这种现象，一种可行的解释是：以前，人们并不太关心字符编码。在ID3还不支持
Unicode时，广大Windows程序猿们写的程序用系统默认的编码（GB18030）来储存中文标签
，并用同样的方法解码。这样编码的文件，用自己的播放器打开，是可以正确显示的。但是
，一旦在其它平台上打开，如Mac OS X和GNU/Linux，这些平台上的默认字符编码并不是
GB18030，于是，显示出来的就是乱码。ID3v2已经支持了Unicode，支持LATIN1、UTF16、
UTF16be、UTF8编码，但或许是这种以Windows为中心的传统被“发扬广大”，新的国产MP3播
放、编码软件仍然不正确地设置字符编码，而是名义上将字符编码设置为LATIN1，而实际上
用GB18030编码。

There is a possible explanation to this phenomenon. In the past, people do not
pay much attention to character encoding. At the time when ID3 did not yet
support Unicode, the majority of Windows programmers use the system's default
character encoding (it is GB18030 for the Chinese version of Windows) for ID3
tags that contain Chinese characters, and decode using the same encoding. Such
files can be normally opened and displayed using their own MP3 players. However,
once opened on other platforms, such as Mac OS X and GNU/Linux, where the
default character encoding is not GB18030, it will print garbage instead.
ID3v2 already supports Unicode, and support multiple encodings such as
LATIN1, UTF16, UTF16be and UTF8. However, perhaps popularised by those
Windows-centric "traditions", new MP3 players and encoders still do not
correctly set the character encoding. They apparently label the encoding as
LATIN1, but actually encodes the text with GB18030.

这个小脚本读取MP3文件中的ID3标签，并试图将其中的以LATIN1为编码的文本标签按
GB18030重新解码，并储存为UTF16编码。之所以选用UTF16而不是UTF8，是因为UTF16编码中
文字符的时候效率比UTF8高33%。为了不局限于中文，这个脚本也提供了命令行选项来指定
源字符集。我只知道中国的网络音乐社区有这种“乱码”现象，不知道其它国家有没有类似的
问题。

This tiny script reads the ID3 tags from MP3 files, attempts to re-decode the
texts labelled as LATIN1 as if they were GB18030, and saves them as UTF16. The
reason why I chose UTF16 rather than UTF8 is because it is 33% more efficient to
encode Chinese characters than UTF8. This script also provided a command line
option to specify the source encoding so that it can be not too
Chinese-specific. I only know such phenomenon exists in the Chinese Internet
music community, and I am not sure whether other countries have similar problems
or not.

# 使用 Usage

你需要Python3和mutagen库。

You need Python3 and the mutagen library.

```bash
$ pip3 install mutagen
```

用以下命令运行修复文件。其中`-n`选项的作用是“模拟运行”，即：打印出转换的效果，
但不真的写入文件。

Use the following command to repair files. The `-n` option means "dry run", i.e.
printing the results without actually writing into the files.

```bash
$ python3 chineseid3fix.py -n my_mp3_file.mp3
```

如果想真的写入文件，去掉`-n`选项即可。

Remove the `-n` to actually write into the files.

使用`-s`选项来指定源字符集，即：如果文件里标称是LATIN1，那么就把它当成这个字符编
码。

Use the `-s` option to specify the source encoding, i.e. if it is labelled as
LATIN1 in the file, consider it as this encoding.

```bash
$ python3 chineseid3fix.py -s utf8 my_mp3_file.mp3
```

# 作者 Author

王坤山 Kunshan Wang <wks1986@gmail.com>

<!--
vim: tw=80 spell formatoptions+=mM
-->
