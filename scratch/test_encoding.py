text = 'ë† ë¶€ì ˜ ì•„ë‚´ëŠ”'
try:
    fixed = text.encode('cp1252').decode('utf-8')
    print('Fixed (cp1252):', fixed)
except Exception as e:
    print('Failed cp1252:', e)
try:
    fixed = text.encode('latin-1').decode('utf-8')
    print('Fixed (latin-1):', fixed)
except Exception as e:
    print('Failed latin-1:', e)
