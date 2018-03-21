if exists('g:loaded_neortags')
   finish
endif

let g:loaded_neortags = 1

noremap <Leader>mf :NeortagsFindReferences<CR>
noremap <Leader>mv :NeortagsFindVirtuals<CR>
noremap <Leader>mj :NeortagsJumpTo<CR>
noremap <Leader>mi :NeortagsSymbolInfo<CR>
noremap <Leader>mp :NeortagsPreprocess<CR>
noremap <Leader>mh :NeortagsClassHierarchy<CR>
