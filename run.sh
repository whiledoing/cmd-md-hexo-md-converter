#!/bin/bash

PWD=`cd $(dirname $0); pwd;`
HEXO_BLOG_DIR="$HOME/work/proj/hexo-blog"
HEXO_POST_DIR="$HEXO_BLOG_DIR/source/_posts"

(
    cd $PWD
    python converter.py $HEXO_POST_DIR all
)
