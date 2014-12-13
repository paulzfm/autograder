import sys
import os
import filecmp
import datetime

class Grader:
	def runStdProgram(self):
		count = 0
		for sample in self.samples:
			count += 1
			print 'Running standard program (%i/%i) ...' % (count, len(self.samples))
			stdoutput = os.path.join(self.outputFolder, '%s.stdout' % (os.path.basename(sample)))
			ret = os.system('%s < %s > %s' % (self.std, sample, stdoutput))
			ret /= 256
			if ret != 0:
				print '*** Error: Standard program exit with code %i' % ret
				sys.exit(1)

	def test(self):
		print '\nBegin test...\n'
		count = 0
		for sample in self.samples:
			count += 1
			myoutput = os.path.join(self.outputFolder, '%s.out' % (os.path.basename(sample)))
			start = datetime.datetime.now()
			ret = os.system('%s < %s > %s' % (self.my, sample, myoutput))
			end = datetime.datetime.now()
			tcost = (end - start).microseconds
			tcost /= 1000.0
			result = ''
			ret /= 256
			if ret != 0:
				result = 'Runtime Error: %i' % ret

			stdoutput = os.path.join(self.outputFolder, '%s.stdout' % (os.path.basename(sample)))
			if filecmp.cmp(stdoutput, myoutput):
				result = 'OK :)'
			else:
				result = 'Wrong'

			print '%i\t[%s]\t%s\t%.2fms' % (count, os.path.basename(sample), result, tcost)

	def ctrl(self):
		self.samples = []
		ignore = 0
		for f in os.listdir(self.sampleFolder):
			path = os.path.join(self.sampleFolder, f)
			if os.path.isfile(path) and not f.startswith('.') and not f.endswith('~'):
				self.samples.append(path)
			else:
				ignore += 1

		print '%i samples found (%i ignored).' % (len(self.samples), ignore)

		self.runStdProgram()
		self.test()


	def __init__(self, args):
		self.std = args[1]
		self.my = args[2]
		self.sampleFolder = args[3]
		if len(args) == 5:
			self.outputFolder = args[4]
		else:
			self.outputFolder = 'output/'

		if not os.path.exists(self.std):
			print '***Error: Standard program [%s] not found.' % self.std
			sys.exit(1)

		if not os.path.exists(self.my):
			print '***Error: Your program [%s] not found.' % self.my
			sys.exit(1)

		if not os.path.exists(self.sampleFolder):
			print '***Error: Sample folder [%s] not found.' % self.sampleFolder
			sys.exit(1)

		if not os.path.exists(self.outputFolder):
			os.mkdir(self.outputFolder)

		self.ctrl()


if __name__ == '__main__':
	if len(sys.argv) != 4 and len(sys.argv) != 5:
		print 'Usage: python %s stdProgram myProgram sampleFolder [outputFolder]' % sys.argv[0]
		sys.exit(1)

	grader = Grader(sys.argv)
