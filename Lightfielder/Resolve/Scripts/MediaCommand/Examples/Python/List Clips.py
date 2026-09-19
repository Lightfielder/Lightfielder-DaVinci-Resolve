# Media Command Script

print("\n\n[List Clips]")
dct = bmd.readstring(args)
for clipIndex, clipValue in dct.iteritems():
    print(clipValue["Clip Name"])
