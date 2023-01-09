from .rotatebrushtip import Rotatebrushtip

# And add the extension to Krita's list of extensions:
app = Krita.instance()
# Instantiate your class:
extension = Rotatebrushtip(parent = app)
app.addExtension(extension)
