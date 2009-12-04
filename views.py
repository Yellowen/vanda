from django.shortcuts import render_to_response as rr


#!!! TODO: this view is just for testing and shall remove on release time.
#REMOVE:START --------------------------------------
def testview (requset ):
    return rr ('test/index.html')



#REMOVE:END----------------------------------
