if exists('g:loaded_neortags')
   finish
endif

let g:loaded_neortags = 1

noremap <Leader>mf :call NeortagsFindReferences()<CR>
noremap <Leader>mj :call NeortagsJumpTo()<CR>
noremap <Leader>mi :call NeortagsSymbolInfo()<CR>
noremap <Leader>mp :call NeortagsPreprocess()<CR>
