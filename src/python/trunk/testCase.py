from testCase import testCase
import time,os
"""
testCase.srcPicFileList = testCase.getFileList('./testPIC/srcPic/allFormat/*')
for i in range( len( testCase.srcPicFileList ) ):
    testCase.srcPicFileList[i] = testCase.srcPicFileList[i].replace('./testPIC/srcPic/allFormat/','')
#print testCase.srcPicFileList
#os.sys.exit(1)

t1 = time.time()
testCase.testOldConvert.runTestPic()
t2 = time.time()


t3 = time.time()
testCase.testNewConvert.runTestPic()
t4 = time.time()
print "old convert end! runTIme:%s" % (t2-t1)
print "lib convert end! runTIme:%s" % (t4-t3)
"""


testCase.srcPicFileList = testCase.getFileList('./testPIC/srcPic/allFormat/*')
for i in range( len( testCase.srcPicFileList ) ):
    testCase.srcPicFileList[i] = testCase.srcPicFileList[i].replace('./testPIC/srcPic/allFormat/','')
print testCase.srcPicFileList

t1 = time.time()
testCase.testOldConvert.testAllFormatRun()
t2 = time.time()

t3 = time.time()
testCase.testNewConvert.testAllFormatRun()
t4 = time.time()

t5 = time.time()
testCase.testNewConvert10.testAllFormatRun()
t6 = time.time()
print "old gif all format convert end! runTIme:%s" % (t2-t1)
print "lold gif all format convert end! runTIme:%s" % (t4-t3)
print "lold gif all format convert10 end! runTIme:%s" % (t6-t5)