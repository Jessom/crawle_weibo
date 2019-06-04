#!/usr/bin/env sh

# 确保脚本抛出遇到的错误
set -e

# 爬取微博内容
python3 weibo.py

# 解析微博，生成图表
python3 analysis.py

# 解析微博，生成词云图
python3 main.py

cd -