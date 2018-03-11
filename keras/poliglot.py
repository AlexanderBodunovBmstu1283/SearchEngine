import poliglo
from poliglo.text import Text as T
text = T("это очень плохо. А это намного лучше, даже хорошо!")
print(text.polarity)
for s in text.sentences:
    print( s, s.polarity)