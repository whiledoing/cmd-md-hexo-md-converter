#!/bin/bash

PWD=`cd $(dirname $0); pwd;`
HEXO_BLOG_DIR="$HOME/work/proj/hexo-blog"
HEXO_POST_DIR="$HEXO_BLOG_DIR/source/_posts"

(
    cd $PWD
    python converter.py $HEXO_POST_DIR all
)

(
    if [[ $# < 1 ]]; then
        exit 0
    fi

    # wrapper for hexo operation
    # g(generate) s(server) d(deploy) o(open url)
    cd $HEXO_BLOG_DIR
    hexo_con_charas=$1
    for ((i=0; i<${#hexo_con_charas}; i++)); do
        case "${hexo_con_charas:$i:1}" in
            g)
                hexo generate
                ;;
            s)
                hexo server
                ;;
            d)
                hexo deploy
                ;;
            o)
                open http://localhost:4000
                ;;
            h)
                hexo server &> /dev/null &
                ;;
            *)
                echo "invalid control chara for hexo, valid control is [g|s|d]"
                exit 1
                ;;
        esac
    done
)
