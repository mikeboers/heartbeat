import sys

print >> sys.stderr, 'loading app config'

def on_reload(server):
    print >> sys.stderr, 'on_reload(%r)' % server

def when_ready(server):
    print >> sys.stderr, 'when_ready(%r)' % server
