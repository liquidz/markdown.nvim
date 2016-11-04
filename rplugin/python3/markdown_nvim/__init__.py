import neovim
import markdown
from pprint import pformat

@neovim.plugin
class MarkdownNvim(object):
    def __init__(self, vim):
        self.__vim = vim
        self.__md = markdown.Markdown()
        self.__tmp = '/tmp/.markdown_nvim.html'
        self.__previewing = False

    def __echo(self, data):
        self.__vim.command("echo '[markdown.nvim] {}'".format(pformat(data).replace("'", "\"")))

    def __previewable(self):
        try:
            if self.__vim.eval('g:neoterm_loaded') == 1 and self.__vim.eval('executable("w3m")') == 1:
                return True
            return False
        except Exception:
            return False

    def __refresh_preview(self):
        if self.__previewing:
            self.__vim.command('T R')

    @neovim.autocmd('TextChangedI', pattern='*.md', sync=False)
    def __buf_write(self):
        buf = self.__vim.current.buffer
        res = self.__md.convert("\n".join(buf[:]))
        wfp = open(self.__tmp, 'w')
        wfp.write(res)
        wfp.close()
        self.__refresh_preview()

    @neovim.command("MarkdownPreview")
    def __preview(self):
        if self.__previewable():
            self.__vim.command('T w3m {}'.format(self.__tmp))
            self.__previewing = True
        else:
            self.__echo('neoterm and w3m are needed to preview')
