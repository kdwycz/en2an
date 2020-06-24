# en2an: Chinese Numerals To Arabic Numerals

[![Pypi](https://img.shields.io/pypi/v/en2an.svg)](https://pypi.org/project/en2an/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/Ailln/en2an/blob/master/LICENSE)
[![stars](https://img.shields.io/github/stars/Ailln/en2an.svg)](https://github.com/Ailln/en2an/stargazers)
[![API](https://img.shields.io/badge/API-reference-pink.svg)](https://github.com/Ailln/en2an/wiki/API)

📦 **`en2an`** 是一个快速转化 `英文数字` 和 `阿拉伯数字` 的工具包！

## 1 功能

### 1.1 `英文数字` => `阿拉伯数字`

### 1.2 `阿拉伯数字` => `英文数字`

### 1.3 句子转化（试验性功能）

### 1.4 其他

- 支持小数
- 支持负数

## 2 安装

> ⚠️注意：
> 1. 仅支持 Python 的 3.6 以上版本；
> 2. 请安装使用 en2an 的最新版本。

### 2.1 使用 pip 安装

```shell
pip install en2an
```

### 2.2 从代码库安装

```shell
git clone https://github.com/Ailln/en2an.git
cd en2an && python setup.py install
```

## 3 使用

```python
# 在文件首部引入包
import en2an

# 查看版本
print(en2an.__version__)
# 0.0.1
```

## 4 版本支持

- 理论上支持 `Windows`、`MacOS`、`Ubuntu` 下的所有 `Python 3.6+` 的版本。
- 实际上仅在 `Windows 10`、`MacOS 10.14`、`Ubuntu 16.04` 的 `Python 3.6.9` 和 `Python3.7.4` 上做过完整测试。
- 欢迎提交其他版本使用情况到 [Issues](https://github.com/Ailln/en2an/issues) 中，期待你的反馈。
- 如果你有 `Python 2` 的使用需求，可 Fork 代码自行修改。当然也欢迎提 PR，贡献自己代码给其他人。

## 5 问题反馈

1. 先搜索 [Issues](https://github.com/Ailln/en2an/issues) 中有没有人已经问过类似的问题；
2. 如果没有找到解答，请新开一个 issue：
    1. 首先，在「issue 标题」中填写你遇到的问题的简介；
    2. 然后，在「issue 详情」中填写你遇到的问题的详情；
    3. 最后，不要忘记注明你使用的操作系统（比如 Windows 10）和 Python 版本（比如 Python 3.6.3）。
3. 还可以参考 [issue 模版](https://github.com/Ailln/en2an/tree/master/.github/ISSUE_TEMPLATE)。

## 7 许可证

[![](https://award.dovolopor.com?lt=License&rt=MIT&rbc=green)](./LICENSE)

## 8 交流

欢迎添加微信号：`Ailln_`，备注「en2an」，我邀请你进入交流群。