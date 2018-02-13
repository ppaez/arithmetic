" Vim global plugin for arithmetic
" Last Change:  2018 Fed 05
" Maintainer:   Patricio Paez
" License:      GNU General Public License version 2 or later


" wrapper
function! s:Calculate()
python3 << endOfPython

from wrapper import calculate

print(calculate())

endOfPython
endfunction

" Map F5 by default
if !hasmapto('<Plug>ArithmeticCalculate')
   map <unique> <F5> <Plug>ArithmeticCalculate
   map! <unique> <F5> <Plug>ArithmeticCalculate
endif
noremap <unique> <script> <Plug>ArithmeticCalculate <SID>Calculate
noremap <SID>Calculate :call <SID>Calculate()<CR>
noremap! <unique> <script> <Plug>ArithmeticCalculate <SID>Calculate
noremap! <SID>Calculate <ESC>:call <SID>Calculate()<CR>

" Add Plugin -> Arithmetic menus
noremenu <script> &Plugin.&Arithmetic.&Calculate<Tab>:Calculate <SID>Calculate
noremenu <script> &Plugin.&Arithmetic.&Tutorial :edit $HOME/.vim/doc/arithmetic/tutorial.txt<CR>
noremenu <script> &Plugin.&Arithmetic.&Help :help arithmetic<CR>

" User command
if !exists(":Calculate")
   command Calculate :call s:Calculate()
endif