#/bin/python
#-*- encoding: utf-8 -*-

import os
import sys
import shutil

FIRST_N_LINE_FOR_HEADER_CHECK = 30
CHAPTER_MARKER = '#'
SEP_MARKER = '---'
TITLE_MARKER = '==='

def log_info(msg):
    print '[INFO] %s' % msg
    
def log_error(msg):
    print '[ERROR] %s' % msg

class ConverterError(Exception):
    def __init__(self, msg = None):
        self.msg = msg

    def __str__(self):
        class_name = self.__class__.__name__
        return '%s : %s' % (class_name, self.msg) if self.msg else '%s' % class_name

class NoTitleFound(ConverterError):
    pass

class NoValidTagFound(ConverterError):
    pass

class CmdMd2HexoMdConvert(object):
    def __init__(self, copy_to_dst_dir):
        self._cur_dir = os.path.abspath(os.path.curdir)
        self._copy_to_dst_dir = copy_to_dst_dir

        self._src_dir = os.path.join(self._cur_dir, 'cmd-md-src')
        if not os.path.exists(self._src_dir): os.makedirs(self._src_dir)

        self._dst_dir = os.path.join(self._cur_dir, 'nexo-md-dst')
        if not os.path.exists(self._dst_dir): os.makedirs(self._dst_dir)

    def convert_all(self):
        for name in os.listdir(self._src_dir):
            self.convert(name, name)

    def convert(self, src, dst):
        try:
            self._convert_impl(src, dst)
        except ConverterError, e:
            log_error(e)

    def _convert_impl(self, ori_src, ori_dst):
        src = os.path.join(self._src_dir, ori_src)
        if not os.path.exists(src):
            return log_info('invalid src file - %s' % src)

        with open(src) as f_in:
            out_info = self._parse_impl(f_in, src)
            dst = os.path.join(self._dst_dir, ori_dst)
            with open(dst, 'w') as f_out:
                self._write_impl(f_out, dst, out_info)

        log_info('convert success - "%s"' % ori_src)

    def _parse_impl(self, f_in, src):
        # find all header part
        res = {}
        title_line_num = None
        content_line_cache = []
        for line_num, line in enumerate(f_in):
            # more than max header line num
            if line_num >= FIRST_N_LINE_FOR_HEADER_CHECK: break

            # first not empty line should must be title
            if 'title' not in res:
                line = line.strip()
                if not line: continue

                title = line.replace('#', '').strip()
                if not title: raise NoTitleFound('src file "%s"' % src)

                # I don't know why the cmd-markdown-editor insert three charc in the title, so remove it manaully
                # [ref](http://stackoverflow.com/questions/1972362/why-is-my-bash-script-adding-feff-to-the-beginning-of-files)
                title = title[3:]
                if not title: raise NoTitleFound('src file "%s"' % src)

                res['title'] = title
                title_line_num = line_num
                continue

            # ignore title === mark if this is the line just after title
            if (title_line_num + 1 == line_num) and line.startswith(TITLE_MARKER): continue

            # check is another control info
            if line.startswith('tags:') or line.startswith('Tags:'): 
                tags = line[5:].strip().split()
                if not tags: raise NoValidTagFound('src file "%s"' % src)
                res['tags'] = tags

                # if find tags, then pop all the cache, become not find to the real content
                content_line_cache = []
            else:
                content_line_cache.append(line)

        # must has title
        if 'title' not in res: raise NoTitleFound('src file "%s"' % src)

        # join all line cache and all the other real content lines
        res['content'] = content_line_cache + list(f_in)
        return res

    def _write_impl(self, f_out, dst, out_info):
        out_md_list = []
        out_md_list.append(SEP_MARKER)
        out_md_list.append('title: %s' % out_info.get('title', ''))

        if 'tags' in out_info:
            out_md_list.append('tags: [%s]' % ','.join(out_info['tags']))

        out_md_list.append(SEP_MARKER)

        # append content
        for line in out_info['content']:
            if line.startswith('[TOC]'):
                out_md_list.append('<!-- toc -->')
            else:
                out_md_list.append(line.rstrip())

        f_out.write('\n'.join(out_md_list))

        # copy to global dst dir
        shutil.copy2(dst, os.path.join(self._copy_to_dst_dir, os.path.basename(dst)))

def help():
    print '\n'.join([
    'convert cmd-markdown-editor md to hexo-compatible-markdonw format',
    '',
    'example:',
    '---',
    'python convert.py %copy_all_dst_to_dire [last N]|[all]',
    '---'
    ])
    
def run():
    if len(sys.argv) <= 1: return help()

    cp_file_dir_path = sys.argv[1]
    if not os.path.exists(cp_file_dir_path): os.makedirs(cp_file_dir_path)

    if len(sys.argv) == 3 and sys.argv[2] == 'all':
        return CmdMd2HexoMdConvert(cp_file_dir_path).convert_all()

    return help()

if __name__ == '__main__':
    run()

