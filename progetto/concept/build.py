import os,sys
here=os.path.dirname(os.path.abspath(__file__))
logo=open(sys.argv[1]).read()
os.makedirs(os.path.join(here,'dist'),exist_ok=True)
for f in os.listdir(here):
    if f.endswith('.html'):
        s=open(os.path.join(here,f)).read().replace('%%LOGO%%',logo)
        open(os.path.join(here,'dist',f),'w').write(s); print('built',f,len(s))
