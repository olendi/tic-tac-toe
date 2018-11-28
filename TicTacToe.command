#!/usr/bin/env python

import ui

app = ui.TicTacToe()
app.master.title('Baba Tic-Tac-Toe')

app.master.attributes('-topmost', True)
app.master.update()
app.master.attributes('-topmost', False)

app.mainloop()
