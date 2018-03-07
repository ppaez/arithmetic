;; This buffer is for text that is not saved, and for Lisp evaluation.
;; To create a file, visit it with C-x C-f and enter text in its buffer.

;;(delete-region 1 10)


;;(string (char-after))a


;; (start-process "arithmetic" "foo" "python" "-m" "/home/pp/Downloads/src/arithmetic/arithmetic.py")

;; (kill-buffer "foo")

(defun calculate ()
  "calculate using arithmetic"
  (interactive)
  (set 'myfolder (file-name-directory (symbol-file 'calculate)))
  (set 'module (concat myfolder "arithmetic.py"))
  (set 'aprocess (start-process "arithmetic" "foo" "/usr/bin/python3" module))
  (save-current-buffer
     (set-buffer "foo")
     (erase-buffer)
     )
   (set 'mytext (buffer-substring (point-min) (point-max)))
   (process-send-string aprocess mytext)
   (process-send-eof aprocess)
   (accept-process-output aprocess 2)
   (save-current-buffer
     (set-buffer "foo")
     (set 'result (buffer-substring (point-min) (point-max)))
     )
   (set 'mypoint (point))
   (erase-buffer)
   (insert result)
   (goto-char mypoint)
   )


(global-set-key (kbd "<f5>") 'calculate)
