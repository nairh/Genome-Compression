import pandas

def fromFile( filename ):
	print("Reading data from: ", filename)
	chunks = []
	genomes = pandas.read_csv( filename, chunksize = 100, index_col = 'Sample' )
	for chunk in genomes:
		chunks.append( chunk )
	genomes = pandas.concat( chunks )

	rootRef = genomes.ix['reference']['Sequence']
	genomes.drop( 'reference', inplace = True )	

	dataset = genomes.as_matrix( ['Sequence'] ).ravel()

	print('Done reading data.')
	return dataset.tolist(), rootRef

