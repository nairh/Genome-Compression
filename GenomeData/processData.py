import pandas
import sys
import os

def processGenotype( genotype, reference, alternate ):
	print( len(genotype), len(reference), len(alternate) )
	bases = []
	for index,base in enumerate(genotype):
		if base == '0':
			bases.append( reference[index] )
		if base == '1':
			bases.append( alternate[index] )
	return ''.join(bases)

def readGenomes( datapath, reference, alternate, samplePrefix, outfile ):
	genomes_df = pandas.DataFrame( columns = ('Sample', 'Sequence') )
	ref = pandas.read_csv(datapath + '/' + reference)['ref'][0]
	alt = pandas.read_csv(datapath + '/' + alternate)['alt'][0]

	genomes_df = genomes_df.append( { 'Sample': 'reference', 'Sequence': ref }, ignore_index = True )

	for filename in os.listdir( datapath ):
		if filename.startswith( samplePrefix ):
			print( 'Reading file: ', filename )
			for sample in pandas.read_csv(datapath + '/' + filename).itertuples():
				genomes_df = genomes_df.append( { 'Sample': sample[1] + '_1', 
									'Sequence': processGenotype(sample[2], ref, alt) },
								    ignore_index = True)
				genomes_df = genomes_df.append( { 'Sample': sample[1] + '_2', 
								    'Sequence': processGenotype(sample[3], ref, alt) },
								    ignore_index = True)

	print( 'Writing output to: ', outfile)
	genomes_df.to_csv( outfile, compression = 'gzip', chunksize = 50)

filepath = sys.argv[1]
outfile = sys.argv[2]
readGenomes( filepath, "Reference.csv", "Alternate.csv", "SampleGenotype_", outfile)
