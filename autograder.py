import sys
import os
import filecmp
import datetime

class Grader:
	def run(self, sample):
		stdoutput = os.path.join(self.outputFolder, '%s_std.out' % (os.path.basename(sample)))
		ret1 = os.system('%s < %s > %s' % (self.std, sample, stdoutput))
		ret1 /= 256
		if ret1 != 0:
			print '*** Error: Stardard program exit with code %i' % ret1
			sys.exit(1)
		
		myoutput = os.path.join(self.outputFolder, '%s_my.out' % (os.path.basename(sample)))
		start = datetime.datetime.now()
		ret2 = os.system('%s < %s > %s' % (self.my, sample, myoutput))
		end = datetime.datetime.now()
		t = (end - start).microseconds
		ret2 /= 256
		if ret2 != 0:
			return ('Runtime Error: %i' % ret2, time)

		if filecmp.cmp(stdoutput, myoutput):
			return ('Correct', t)
		else:
			return ('Wrong', t)

	def ctrl(self):
		self.samples = []
		ignore = 0
		for f in os.listdir(self.sampleFolder):
			path = os.path.join(self.sampleFolder, f)
			if os.path.isfile(path) and (not f.startswith('.')):
				self.samples.append(path)
			else:
				ignore += 1

		print '%i samples found (%i ignored).' % (len(self.samples), ignore) 

		count = 0
		for sample in self.samples:
			count += 1
			results = self.run(sample)
			print '%i\t[%s]\t\t%s\t\t%.1fms' % (count, os.path.basename(sample), results[0], results[1] / 1000.0)


	def __init__(self, args):
		self.std = args[1]
		self.my = args[2]
		self.sampleFolder = args[3]
		self.outputFolder = args[4]
		if not os.path.exists(self.outputFolder):
			os.mkdir(self.outputFolder)

		self.ctrl()


if __name__ == '__main__':
	if len(sys.argv) != 5:
		print 'Usage: python %s stdProgram myProgram sampleFolder outputFolder' % sys.argv[0]
		sys.exit(1)

	grader = Grader(sys.argv)
